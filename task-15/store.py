from collections import defaultdict

class EventStore:
    def __init__(self):
        self.store = defaultdict(list)

    def append(self, aggregate_id, event):
        self.store[aggregate_id].append(event)
        print(f"[EVENT STORE] Appended: {event.name}")

    def get_events(self, aggregate_id):
        return self.store[aggregate_id]

    def replay(self, aggregate_id):
        events = self.get_events(aggregate_id)

        state = {"status": None, "total": 0}

        for e in events:
            if e.name == "OrderPlaced":
                state["status"] = "PLACED"
                state["total"] = e.data["total"]

        return state