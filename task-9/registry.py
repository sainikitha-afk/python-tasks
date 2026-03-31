class Registry:
    def __init__(self):
        self.commands = {}
        self.themes = {}
        self.processors = {}

    def register(self, category, name, value):
        getattr(self, category)[name] = value