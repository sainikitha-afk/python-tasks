from fastapi import FastAPI
import random
import time

app = FastAPI()

@app.get("/users/{id}")
async def get_user(id: int):
    time.sleep(0.1)
    return {"id": id, "name": "Alice"}

@app.get("/orders/{id}")
async def get_order(id: int):
    time.sleep(0.2)

    # simulate failure randomly
    if random.choice([True, False, False]):
        return {"error": "Service failure"}

    return {"id": id, "status": "delivered"}

@app.get("/products/{id}")
async def get_product(id: int):
    time.sleep(0.05)
    return {"id": id, "product": "Laptop"}