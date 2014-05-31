import logging

from deluge.plugins.pluginbase import CorePluginBase


LOGGER = logging.getLogger(__name__)


class Core(CorePluginBase):

    def enable(self):
        """"""
        LOGGER.info('Enabling WebAPI plugin CORE ...')

    def disable(self):
        """"""
        LOGGER.info('Disabling WebAPI plugin CORE ...')

    def update(self):
        """"""
