import logging

from deluge import component
from deluge.plugins.pluginbase import CorePluginBase
from deluge.ui.web.json_api import JSON
from twisted.web import http, server
import deluge.configmanager
from deluge.core.rpcserver import export


LOGGER = logging.getLogger(__name__)

DEFAULT_PREFS = {
    'enable_cors' : False,
    'allowed_origin' : []
}

class Core(CorePluginBase):

    def enable(self):
        """"""
        LOGGER.info('Enabling WebAPI plugin CORE ...')
        self.JSON_instance = component.get('JSON')
        self.patched = False
        self.config = deluge.configmanager.ConfigManager('webapi.conf', DEFAULT_PREFS)
        if self.config['enable_cors']:
            self.patch_web_ui()

    def disable(self):
        """"""
        LOGGER.info('Disabling WebAPI plugin CORE ...')
        self.config.save()

    def update(self):
        """"""

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
        "returns the config dictionary"
        return self.config.config

    def patch_web_ui(self):
        if self.patched:
            return
        LOGGER.info('Patching webui for CORS...')
        self.old_render = self.JSON_instance.render
        self.old_send_request = self.JSON_instance._send_response
        self.JSON_instance.render = self.render_patch
        self.JSON_instance._send_response = self._send_response_patch
        self.patched = True

    def unpatch_web_ui(self):
        if not self.patched:
            return
        LOGGER.info('Unpatching webui for CORS...')
        if self.old_render:
            self.JSON_instance.render = self.old_render
        if self.old_send_request:
            self.JSON_instance._send_response = self.old_send_request
        self.patched = False

    def render_patch(self, request):
        if request.method == 'OPTIONS':
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
        return self.old_render(request)

    def _send_response_patch(self, request, response):
        if request._disconnected:
            return ''
        origin = request.getHeader('Origin')
        if origin in self.config['allowed_origin']:
            request.setHeader('Access-Control-Allow-Origin', origin)
            request.setHeader('Access-Control-Allow-Credentials', 'true')
        return self.old_send_request(request, response)
