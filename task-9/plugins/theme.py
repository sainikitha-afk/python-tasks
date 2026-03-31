class Plugin:
    name = "dark-mode-theme"
    dependencies = []

    def activate(self, registry):
        registry.register("themes", "dark-mode", "Dark Theme")

    def deactivate(self):
        pass