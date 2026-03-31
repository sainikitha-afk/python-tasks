from datetime import datetime


class Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.timestamp = datetime.utcnow()


class OrderPlaced(Event):
    def __init__(self, order_id, customer, total, items):
        super().__init__("OrderPlaced", {
            "order_id": order_id,
            "customer": customer,
            "total": total,
            "items": items
        })