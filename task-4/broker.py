import redis
import json
import uuid
import time

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

QUEUE = "task_queue"
DEAD = "dead_letter"
RESULT = "results"


def enqueue(func, **kwargs):
    task = {
        "id": str(uuid.uuid4())[:6],
        "func": func,
        "args": kwargs,
        "retries": 0,
        "max_retries": 3,
        "status": "PENDING",
        "created_at": time.time()
    }

    r.lpush(QUEUE, json.dumps(task))

    print(f'Task queued: <Task id={task["id"]} func={func} status=PENDING>')