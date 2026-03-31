class Plugin:
    name = "markdown-parser"
    dependencies = []

    def activate(self, registry):
        registry.register("processors", ".md", "Markdown -> HTML")