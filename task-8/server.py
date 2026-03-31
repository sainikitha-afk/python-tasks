from fastapi import FastAPI, WebSocket
import asyncio
import random
import pandas as pd
import numpy as np
from datetime import datetime

app = FastAPI()

clients = []
data_buffer = []

THRESHOLD = 100

# -----------------------------
# SENSOR DATA GENERATOR
# -----------------------------
async def sensor_stream():
    while True:
        temp = round(random.uniform(70, 110), 2)
        vibration = round(random.uniform(0.1, 0.6), 2)

        record = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "temp": temp,
            "vibration": vibration
        }

        data_buffer.append(record)

        if len(data_buffer) > 50:
            data_buffer.pop(0)

        df = pd.DataFrame(data_buffer)

        avg = df["temp"].mean()
        std = df["temp"].std() if df["temp"].std() != 0 else 1
        z_score = (temp - avg) / std

        status = "NORMAL"
        if temp > THRESHOLD:
            status = "CRITICAL"
        elif z_score > 2:
            status = "WARNING"

        payload = {
            "time": record["time"],
            "temp": temp,
            "avg": round(avg, 2),
            "status": status
        }

        print(f"[{record['time']}] temp={temp} avg={round(avg,2)} status={status}")

        for ws in clients:
            await ws.send_json(payload)

        await asyncio.sleep(1)


# -----------------------------
# WEBSOCKET
# -----------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    print("[INFO] Client connected")

    try:
        while True:
            await ws.receive_text()
    except:
        clients.remove(ws)
        print("[INFO] Client disconnected")


# -----------------------------
# STARTUP
# -----------------------------
@app.on_event("startup")
async def startup():
    asyncio.create_task(sensor_stream())
    print("[INFO] Stream started at http://localhost:8000")