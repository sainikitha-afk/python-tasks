class ReadStore:
    def __init__(self):
        self.db = {}

    def insert(self, order_id, data):
        self.db[order_id] = data

    def get(self, order_id):
        return self.db.get(order_id)