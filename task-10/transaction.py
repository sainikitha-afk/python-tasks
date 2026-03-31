class Transaction:
    def __init__(self, sender, receiver, amount, signature=""):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def __repr__(self):
        return f"{self.sender[:6]} -> {self.receiver[:6]} : {self.amount}"