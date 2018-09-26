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

        component.get("Preferences").add_page("WebAPI", self.glade.get_widget("prefs_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)

        self.glade.get_widget('add_button').connect("clicked", self.add_domain)
        self.glade.get_widget('remove_button').connect("clicked", self.remove_domain)
        self.glade.get_widget('remove_all_button').connect("clicked", self.remove_all_domain)
        self.create_listview()

    def disable(self):
        """Triggers when plugin is disabled."""
        LOGGER.info('Disabling WebAPI plugin GTK ...')

        component.get("Preferences").remove_page("WebAPI")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

    def on_apply_prefs(self):
        log.debug("applying prefs for WebAPI")
        config = {}
        if self.glade.get_widget("enable_cors").get_active():
            config["enable_cors"] = True
        else:
            config["enable_cors"] = False

        config["allowed_origin"] = []
        if len(self.model) != 0:
            # remove all the entries in the model
            for i in range(len(self.model)):
                iter = self.model.get_iter(i)
                config["allowed_origin"].append(self.model[iter][0])

        client.webapi.set_config(config)

    def on_show_prefs(self):
        client.webapi.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "callback for on show_prefs"
        log.debug("callback for on show_prefs")

        self.glade.get_widget("enable_cors").set_active(config["enable_cors"])
        if len(self.model) != 0:
            # remove all the entries in the model
            for i in range(len(self.model)):
                iter = self.model.get_iter(0)
                self.model.remove(iter)
        for domain in config["allowed_origin"]:
            self.model.append([domain])

    def create_listview(self):
        self.model = gtk.ListStore(str)
        self.list = self.glade.get_widget('treeview1')
        self.list.set_model(self.model)

        parent = self.list.get_parent()
        parent.remove(self.list)
        self.scrollTree = self.glade.get_widget('scrolledwindow1')
        self.scrollTree.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.scrollTree.add(self.list)

        column = gtk.TreeViewColumn('domain', gtk.CellRendererText(), text=0)
        column.set_clickable(True)
        column.set_resizable(True)
        self.list.append_column(column)

        self.selection = self.list.get_selection()
        self.list.get_selection().connect("changed", self.on_changed)

    def on_changed(self, selection):
        pass

    def add_domain(self, button):
        domain = self.glade.get_widget('new_domain').get_text()
        self.model.append([domain])

    def remove_domain(self, button):
        # if there is still an entry in the model
        if len(self.model) != 0:
            # get the selection
            (model, iter) = self.selection.get_selected()
            if iter is not None:
                self.model.remove(iter)

    def remove_all_domain(self, button):
        # if there is still an entry in the model
        if len(self.model) != 0:
            # remove all the entries in the model
            for i in range(len(self.model)):
                iter = self.model.get_iter(0)
                self.model.remove(iter)