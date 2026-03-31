class EventBus:
    def __init__(self):
        self.handlers = []

    def register(self, handler):
        self.handlers.append(handler)

    async def publish(self, events):
        for event in events:
            print(f"[BUS] Publishing {event.name}")
            for handler in self.handlers:
                await handler(event)