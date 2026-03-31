import asyncio
import uuid

from commands import PlaceOrderCommand
from events import OrderPlaced
from store import EventStore
from bus import EventBus
from read_model import ReadStore
from handlers import dashboard_handler, notification_handler, analytics_handler


event_store = EventStore()
bus = EventBus()
read_store = ReadStore()


# Register handlers
bus.register(lambda e: dashboard_handler(e, read_store))
bus.register(notification_handler)
bus.register(analytics_handler)


async def handle_command(cmd):
    print("\n=== Command Side ===")
    print("[WRITE] Processing command")

    order_id = f"ORD-{uuid.uuid4().hex[:4]}"

    total = sum(i["qty"] * i["price"] for i in cmd.items)

    event = OrderPlaced(order_id, cmd.customer_id, total, cmd.items)

    event_store.append(order_id, event)

    await bus.publish([event])

    return order_id


async def main():
    cmd = PlaceOrderCommand(
        "C-42",
        [
            {"sku": "W1", "qty": 2, "price": 50},
            {"sku": "G1", "qty": 1, "price": 100}
        ]
    )

    order_id = await handle_command(cmd)

    print("\n=== Query Side ===")
    print(read_store.get(order_id))

    print("\n=== Event Replay ===")
    events = event_store.get_events(order_id)

    for e in events:
        print(f"{e.name} -> {e.data}")

    print("\nRebuilt state:", event_store.replay(order_id))


if __name__ == "__main__":
    asyncio.run(main())