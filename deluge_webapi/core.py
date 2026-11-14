import logging

import deluge.configmanager
from deluge.core.rpcserver import export
from deluge.plugins.pluginbase import CorePluginBase

from .common import DEFAULT_PREFS

LOGGER = logging.getLogger(__name__)


class Core(CorePluginBase):

    def enable(self):
        LOGGER.info('Enabling WebAPI plugin CORE ...')

        self.config = deluge.configmanager.ConfigManager('webapi.conf', DEFAULT_PREFS)

    def disable(self):
        LOGGER.info('Disabling WebAPI plugin CORE ...')

        self.config.save()

    @export
    def set_config(self, config):
        """sets the config dictionary"""

        for key in config.keys():
            self.config[key] = config[key]

        self.config.save()

    @export
    def get_config(self):
        return self.config.config
