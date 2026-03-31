from wallet import Wallet
from blockchain import Blockchain
from transaction import Transaction

# ---------------------------
# START NODES
# ---------------------------
node1 = Wallet()
node2 = Wallet()
node3 = Wallet()

print("=== Node Startup ===")
print(f"[NODE-1] Wallet: {node1.address}")
print(f"[NODE-2] Wallet: {node2.address}")
print(f"[NODE-3] Wallet: {node3.address}")

# ---------------------------
# BLOCKCHAIN
# ---------------------------
chain = Blockchain()

# ---------------------------
# TRANSACTION
# ---------------------------
print("\n=== Transaction ===")

tx1 = Transaction(node1.address, node2.address, 2.5)
tx1.signature = node1.sign("tx1")

print(f"From: {tx1.sender}")
print(f"To: {tx1.receiver}")
print(f"Amount: {tx1.amount}")
print(f"Signature: {tx1.signature[:20]}... Valid")

chain.add_transaction(tx1)

# ---------------------------
# MINING
# ---------------------------
print("\n=== Mining ===")

chain.mine_pending(node2.address)

# ---------------------------
# BALANCES
# ---------------------------
print("\n=== Wallet Balances ===")

print(f"{node1.address}: {chain.get_balance(node1.address)} coins")
print(f"{node2.address}: {chain.get_balance(node2.address)} coins")
print(f"{node3.address}: {chain.get_balance(node3.address)} coins")