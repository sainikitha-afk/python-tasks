import os
import importlib

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py"):
                module_name = file[:-3]
                module = importlib.import_module(f"{self.plugin_dir}.{module_name}")
                plugin = module.Plugin()
                self.plugins.append(plugin)

    def activate_all(self, registry):
        for plugin in self.plugins:
            plugin.activate(registry)
            print(f"Activated {plugin.name}")