class Plugin:
    name = "rss-feed"
    dependencies = ["markdown-parser"]

    def activate(self, registry):
        registry.register("commands", "generate-rss", "RSS Generator")