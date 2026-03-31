import hashlib
from ecdsa import SigningKey, SECP256k1

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

        self.address = self.generate_address()

    def generate_address(self):
        return "0x" + hashlib.sha256(self.public_key.to_string()).hexdigest()[:12]

    def sign(self, message):
        return self.private_key.sign(message.encode()).hex()