import logging

from gi.repository import Gtk
from deluge import component
from deluge.plugins.pluginbase import Gtk3PluginBase
from deluge.ui.client import client

from .common import get_resource

LOGGER = logging.getLogger(__name__)


class Gtk3UI(Gtk3PluginBase):

    plugin_id = 'WebAPI'

    def enable(self):
        """Triggers when plugin is enabled."""
        LOGGER.info('Enabling WebAPI plugin GTK ...')

        self.builder = Gtk.Builder.new_from_file(get_resource("config.ui"))

        component.get('Preferences').add_page('WebAPI', self.builder.get_object('prefs_box'))
        component.get('PluginManager').register_hook('on_apply_prefs', self.on_apply_prefs)
        component.get('PluginManager').register_hook('on_show_prefs', self.on_show_prefs)

        self.builder.get_object('add_button').connect('clicked', self.add_domain)
        self.builder.get_object('remove_button').connect('clicked', self.remove_domain)
        self.builder.get_object('remove_all_button').connect('clicked', self.remove_all_domain)
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
        if self.builder.get_object('enable_cors').get_active():
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
        self.builder.get_object('enable_cors').set_active(config['enable_cors'])
        self.remove_all_domain()
        for domain in config['allowed_origin']:
            self.model.append([domain])

    def create_listview(self):
        self.model = Gtk.ListStore(str)
        self.list = self.builder.get_object('listview_allowed_domains')
        self.list.set_model(self.model)

        parent = self.list.get_parent()
        parent.remove(self.list)
        self.scrollTree = self.builder.get_object('scrolledwindow_allowed_domains')
        self.scrollTree.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrollTree.add(self.list)

        column = Gtk.TreeViewColumn('domain', Gtk.CellRendererText(), text=0)
        column.set_clickable(True)
        column.set_resizable(True)
        self.list.append_column(column)

        self.selection = self.list.get_selection()

    def add_domain(self, button):
        domain = self.builder.get_object('new_domain').get_text()
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
