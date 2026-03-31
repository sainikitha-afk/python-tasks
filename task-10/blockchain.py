import hashlib
import time

class Block:
    def __init__(self, index, prev_hash, transactions):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.prev_hash}{self.transactions}{self.timestamp}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty):
        print(f"\nMining block #{self.index}...")

        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()

            if self.nonce % 10000 == 0:
                print(f"Nonce: {self.nonce} -> {self.hash[:10]}...")

        print(f"Block mined: {self.hash[:15]}...\n")


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending = []
        self.difficulty = 4
        self.reward = 1.0

        self.create_genesis()

    def create_genesis(self):
        genesis = Block(0, "0", [])
        self.chain.append(genesis)

    def add_transaction(self, tx):
        self.pending.append(tx)

    def mine_pending(self, miner_address):
        reward_tx = {"from": "network", "to": miner_address, "amount": self.reward}
        self.pending.append(reward_tx)

        block = Block(len(self.chain), self.chain[-1].hash, self.pending)
        start = time.time()
        block.mine(self.difficulty)
        end = time.time()

        print(f"Block #{block.index} mined in {round(end-start,2)}s")

        self.chain.append(block)
        self.pending = []

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for tx in block.transactions:
                if isinstance(tx, dict):
                    if tx["to"] == address:
                        balance += tx["amount"]
                else:
                    if tx.receiver == address:
                        balance += tx.amount
                    if tx.sender == address:
                        balance -= tx.amount

        return balance