from plugin_manager import PluginManager
from registry import Registry

print("=== Application Startup ===")

manager = PluginManager()
registry = Registry()

manager.load_plugins()
manager.activate_all(registry)

print("\nRegistered:")
print("Commands:", registry.commands)
print("Themes:", registry.themes)
print("Processors:", registry.processors)