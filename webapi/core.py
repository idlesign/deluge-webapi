import logging

import deluge.configmanager
from deluge import component
from deluge.core.rpcserver import export
from deluge.plugins.pluginbase import CorePluginBase
from twisted.web import http, server

LOGGER = logging.getLogger(__name__)

DEFAULT_PREFS = {
    'enable_cors': False,
    'allowed_origin': [],
}


class Core(CorePluginBase):

    def enable(self):
        LOGGER.info('Enabling WebAPI plugin CORE ...')

        self.patched = False
        self.config = deluge.configmanager.ConfigManager('webapi.conf', DEFAULT_PREFS)

        if self.config['enable_cors']:
            self.patch_web_ui()

    def disable(self):
        LOGGER.info('Disabling WebAPI plugin CORE ...')

        self.config.save()

    @export
    def set_config(self, config):
        """sets the config dictionary"""

        for key in config.keys():
            self.config[key] = config[key]

        self.config.save()

        if self.config['enable_cors']:
            self.patch_web_ui()

        elif not self.config['enable_cors']:
            self.unpatch_web_ui()

    @export
    def get_config(self):
        return self.config.config

    def patch_web_ui(self):

        if self.patched:
            return

        LOGGER.info('Patching webui for CORS...')

        cmp_json = component.get('JSON')

        self.old_render = cmp_json.render
        self.old_send_request = cmp_json._send_response
        cmp_json.render = self.render_patch
        cmp_json._send_response = self._send_response_patch

        self.patched = True

    def unpatch_web_ui(self):

        if not self.patched:
            return

        LOGGER.info('Unpatching webui for CORS...')

        cmp_json = component.get('JSON')
        cmp_json.render = self.old_render
        cmp_json._send_response = self.old_send_request

        self.patched = False

    def render_patch(self, request):

        if request.method != 'OPTIONS':
            return self.old_render(request)

        request.setResponseCode(http.OK)
        origin = request.getHeader('Origin')

        if origin in self.config['allowed_origin']:
            request.setHeader('Access-Control-Allow-Origin', origin)
            request.setHeader('Access-Control-Allow-Headers', 'content-type')
            request.setHeader('Access-Control-Allow-Methods', 'POST')
            request.setHeader('Access-Control-Allow-Credentials', 'true')

        request.write('')
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
