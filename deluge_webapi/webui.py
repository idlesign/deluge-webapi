import logging

import deluge.configmanager
from deluge import component, common
from deluge.plugins.pluginbase import WebPluginBase
from deluge.ui.client import client
from deluge.ui.web.json_api import export as export_api
from twisted.internet.defer import Deferred
from twisted.web import http, server

from .common import DEFAULT_PREFS, get_resource, use_bytes

LOGGER = logging.getLogger(__name__)


class WebUI(WebPluginBase):

    scripts = [get_resource('webapi.js')]

    def enable(self):
        """Triggers when plugin is enabled."""
        LOGGER.info('Enabling WebAPI plugin WEB ...')

        self.patched = False
        self.config = deluge.configmanager.ConfigManager('webapi.conf', DEFAULT_PREFS)

        if self.config['enable_cors']:
            self.patch_web_ui()

    def disable(self):
        """Triggers when plugin is disabled."""
        LOGGER.info('Disabling WebAPI plugin WEB ...')

        self.unpatch_web_ui()

    def patch_web_ui(self):
        """Applies CORS headers patching to the WebUI JSON component."""

        if self.patched:
            return

        LOGGER.info('Patching webui for CORS ...')

        try:
            cmp_json = component.get('JSON')

        except KeyError:
            LOGGER.warning('The JSON component is not available in this process. CORS patching is skipped.')
            return

        self.old_render = cmp_json.render
        self.old_send_request = cmp_json._send_response
        cmp_json.render = self.render_patch
        cmp_json._send_response = self._send_response_patch

        self.patched = True

    def unpatch_web_ui(self):
        """Reverts CORS headers patching of the WebUI JSON component."""

        if not self.patched:
            return

        LOGGER.info('Unpatching webui for CORS ...')

        cmp_json = component.get('JSON')
        cmp_json.render = self.old_render
        cmp_json._send_response = self.old_send_request

        self.patched = False

    def render_patch(self, request):

        if request.method != (b'OPTIONS' if use_bytes else 'OPTIONS'):
            return self.old_render(request)

        request.setResponseCode(http.OK)
        origin = request.getHeader('Origin')

        if origin in self.config['allowed_origin']:
            request.setHeader('Access-Control-Allow-Origin', origin)
            request.setHeader('Access-Control-Allow-Headers', 'content-type')
            request.setHeader('Access-Control-Allow-Methods', 'POST')
            request.setHeader('Access-Control-Allow-Credentials', 'true')

        request.write(b'' if use_bytes else '')
        request.finish()
        return server.NOT_DONE_YET

    def _send_response_patch(self, request, response):

        if request._disconnected:
            return ''

        origin = request.getHeader('Origin')

        if origin in self.config['allowed_origin']:
            request.setHeader('Access-Control-Allow-Origin', origin)
            request.setHeader('Access-Control-Allow-Credentials', 'true')

        return self.old_send_request(request, response)

    @export_api
    def get_torrents(self, ids=None, params=None):
        """Returns information about all or a definite torrent.
        Returned information can be filtered by supplying wanted parameter names.

        """

        if params is None:
            filter_fields = ['name', 'comment', 'hash', 'save_path']
        else:
            if isinstance(params, list):
                filter_fields = params
            else:
                filter_fields = params.replace(" ","").split(",")

        proxy = component.get('SessionProxy')

        filter_dict = {}
        if ids is not None:
            filter_dict['id'] = set(ids).intersection(set(proxy.torrents.keys()))

        document = {
            'torrents': []
        }
        response = Deferred()

        deffered_torrents = proxy.get_torrents_status(filter_dict, filter_fields)

        def on_complete(torrents_dict):
            document['torrents'] = list(torrents_dict.values())
            response.callback(document)
        deffered_torrents.addCallback(on_complete)

        return response

    @export_api
    def add_torrent(self, metainfo, options=None):
        """Adds a torrent with the given options.
        metainfo could either be base64 torrent data or a magnet link.

        Returns `torrent_id` string or None.

        Available options are listed in deluge.core.torrent.TorrentOptions.

        :rtype: None|str
        """
        if options is None:
            options = {}

        coreconfig = component.get('CoreConfig')

        if 'download_location' not in options.keys():
            options.update({'download_location': coreconfig.get("download_location")})

        if common.is_magnet(metainfo):
            LOGGER.info('Adding torrent from magnet URI `%s` using options `%s` ...', metainfo, options)
            result = client.core.add_torrent_magnet(metainfo, options)

        else:
            LOGGER.info('Adding torrent from base64 string using options `%s` ...', options)
            result = client.core.add_torrent_file(None, metainfo, options)

        return result

    @export_api
    def remove_torrent(self, torrent_id, remove_data=False):
        """Removes a given torrent. Optionally can remove data."""
        return client.core.remove_torrent(torrent_id, remove_data)

    @export_api
    def get_api_version(self):
        """Returns WebAPI plugin version."""
        from . import VERSION
        return '.'.join(map(str, VERSION))
