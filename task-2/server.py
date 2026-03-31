import asyncio
import websockets
import json
import uuid

clients = {}
rooms = {"general": set()}

async def notify_users():
    users = list(clients.values())
    message = json.dumps({
        "type": "users",
        "users": users
    })
    for ws in clients:
        await ws.send(message)


async def handler(websocket):
    session_id = str(uuid.uuid4())[:6]
    username = None

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "join":
                username = data["username"]
                clients[websocket] = username
                rooms["general"].add(websocket)

                print(f'[INFO] User "{username}" connected (session: {session_id})')
                print(f'[INFO] {username} joined room #general')

                await notify_users()

            elif data["type"] == "message":
                text = data["message"]

                broadcast = json.dumps({
                    "type": "message",
                    "user": username,
                    "message": text
                })

                for client in rooms["general"]:
                    await client.send(broadcast)

            elif data["type"] == "typing":
                typing_msg = json.dumps({
                    "type": "typing",
                    "user": username
                })

                for client in rooms["general"]:
                    if client != websocket:
                        await client.send(typing_msg)

    except:
        pass
    finally:
        if websocket in clients:
            print(f'[INFO] User "{clients[websocket]}" disconnected')
            rooms["general"].remove(websocket)
            del clients[websocket]
            await notify_users()


async def main():
    print("[INFO] Chat server started on ws://localhost:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())