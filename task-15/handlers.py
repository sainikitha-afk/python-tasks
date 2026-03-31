import asyncio

async def dashboard_handler(event, read_store):
    if event.name == "OrderPlaced":
        print("[HANDLER] Updating dashboard...")
        read_store.insert(event.data["order_id"], {
            "status": "PLACED",
            "total": event.data["total"],
            "customer": event.data["customer"]
        })


async def notification_handler(event):
    if event.name == "OrderPlaced":
        await asyncio.sleep(0.1)
        print("[HANDLER] Email sent!")


async def analytics_handler(event):
    if event.name == "OrderPlaced":
        print("[HANDLER] Analytics updated")