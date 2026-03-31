from broker import enqueue

print("\n=== Producer ===")

enqueue("generate_thumbnail", image_id=4521, size=(256, 256))
enqueue("send_email", to="bob@co.com", template="welcome")