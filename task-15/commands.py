class PlaceOrderCommand:
    def __init__(self, customer_id, items):
        self.customer_id = customer_id
        self.items = items