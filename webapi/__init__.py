VERSION = (0, 2, 1)


try:
    from deluge.plugins.init import PluginInitBase

    class CorePlugin(PluginInitBase):

        def __init__(self, plugin_name):
            from core import Core as _plugin_cls
            self._plugin_cls = _plugin_cls
            super(CorePlugin, self).__init__(plugin_name)


    class GtkUIPlugin(PluginInitBase):

        def __init__(self, plugin_name):
            from gtkui import GtkUI as _plugin_cls
            self._plugin_cls = _plugin_cls
            super(GtkUIPlugin, self).__init__(plugin_name)


    class WebUIPlugin(PluginInitBase):
        def __init__(self, plugin_name):
            from webui import WebUI as _plugin_cls
            self._plugin_cls = _plugin_cls
            super(WebUIPlugin, self).__init__(plugin_name)

except ImportError:
    # That's what we do when this import prevents docs from being built.
    pass