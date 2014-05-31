import logging

from deluge.plugins.pluginbase import GtkPluginBase


LOGGER = logging.getLogger(__name__)


class GtkUI(GtkPluginBase):

    plugin_id = 'WebAPI'

    def enable(self):
        """Triggers when plugin is enabled."""
        LOGGER.info('Enabling WebAPI plugin GTK ...')

    def disable(self):
        """Triggers when plugin is disabled."""
        LOGGER.info('Disabling WebAPI plugin GTK ...')
