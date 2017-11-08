import logging

from twisted.internet.defer import Deferred

from deluge import component, common
from deluge.ui.client import client
from deluge.ui.web.json_api import export as export_api
from deluge.plugins.pluginbase import WebPluginBase

LOGGER = logging.getLogger(__name__)


class WebUI(WebPluginBase):

    def enable(self):
        """Triggers when plugin is enabled."""
        LOGGER.info('Enabling WebAPI plugin WEB ...')

    def disable(self):
        """Triggers when plugin is disabled."""
        LOGGER.info('Disabling WebAPI plugin WEB ...')

    @export_api
    def get_torrents(self, ids=None, params=None):
        """Returns information about all or a definite torrent.
        Returned information can be filtered by supplying wanted parameter names.

        """

        if params is None:
            filter_fields = ['name', 'comment', 'hash', 'save_path']
        else:
            filter_fields = params

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
            document['torrents'] = torrents_dict.values()
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

        metainfo = metainfo.encode()
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
        from webapi import VERSION
        return '.'.join(map(str, VERSION))
