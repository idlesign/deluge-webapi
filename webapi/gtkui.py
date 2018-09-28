import logging
import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from common import get_resource


LOGGER = logging.getLogger(__name__)

class GtkUI(GtkPluginBase):

    plugin_id = 'WebAPI'

    def enable(self):
        """Triggers when plugin is enabled."""
        LOGGER.info('Enabling WebAPI plugin GTK ...')
        self.glade = gtk.glade.XML(get_resource("config.glade"))

        component.get('Preferences').add_page('WebAPI', self.glade.get_widget('prefs_box'))
        component.get('PluginManager').register_hook('on_apply_prefs', self.on_apply_prefs)
        component.get('PluginManager').register_hook('on_show_prefs', self.on_show_prefs)

        self.glade.get_widget('add_button').connect('clicked', self.add_domain)
        self.glade.get_widget('remove_button').connect('clicked', self.remove_domain)
        self.glade.get_widget('remove_all_button').connect('clicked', self.remove_all_domain)
        self.create_listview()

    def disable(self):
        """Triggers when plugin is disabled."""
        LOGGER.info('Disabling WebAPI plugin GTK ...')

        component.get('Preferences').remove_page('WebAPI')
        component.get('PluginManager').deregister_hook('on_apply_prefs', self.on_apply_prefs)
        component.get('PluginManager').deregister_hook('on_show_prefs', self.on_show_prefs)

    def on_apply_prefs(self):
        """Triggers when plugin prefs are apply."""
        config = {}
        if self.glade.get_widget('enable_cors').get_active():
            config['enable_cors'] = True
        else:
            config['enable_cors'] = False

        config['allowed_origin'] = []
        for i, value in enumerate(self.model):
            item = self.model.get_iter(i)
            config['allowed_origin'].append(self.model[item][0])

        client.webapi.set_config(config)

    def on_show_prefs(self):
        """Triggers when plugin prefs are show."""
        client.webapi.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        """callback for on show_prefs"""
        self.glade.get_widget('enable_cors').set_active(config['enable_cors'])
        self.remove_all_domain()
        for domain in config['allowed_origin']:
            self.model.append([domain])

    def create_listview(self):
        self.model = gtk.ListStore(str)
        self.list = self.glade.get_widget('listview_allowed_domains')
        self.list.set_model(self.model)

        parent = self.list.get_parent()
        parent.remove(self.list)
        self.scrollTree = self.glade.get_widget('scrolledwindow_allowed_domains')
        self.scrollTree.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.scrollTree.add(self.list)

        column = gtk.TreeViewColumn('domain', gtk.CellRendererText(), text=0)
        column.set_clickable(True)
        column.set_resizable(True)
        self.list.append_column(column)

        self.selection = self.list.get_selection()

    def add_domain(self, button):
        domain = self.glade.get_widget('new_domain').get_text()
        self.model.append([domain])

    def remove_domain(self, button):
        # if there is still an entry in the model
        if len(self.model) != 0:
            # get the selection
            (model, item) = self.selection.get_selected()
            if item is not None:
                self.model.remove(item)

    def remove_all_domain(self, button=None):
        for i, value in enumerate(self.model):
            item = self.model.get_iter(0)
            self.model.remove(item)