import redis
import json
import time
import importlib

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

QUEUE = "task_queue"
DEAD = "dead_letter"
RESULT = "results"


def execute_task(task, worker_id):
    func_name = task["func"]
    args = task["args"]

    module = importlib.import_module("tasks")
    func = getattr(module, func_name)

    print(f'[WORKER-{worker_id}] Picked up task {task["id"]} ({func_name})')

    start = time.time()

    try:
        result = func(**args)
        duration = round(time.time() - start, 2)

        task["status"] = "SUCCESS"

        r.hset(RESULT, task["id"], json.dumps({
            "func": func_name,
            "status": "SUCCESS",
            "retries": task["retries"],
            "duration": duration
        }))

        print(f'[WORKER-{worker_id}] Task {task["id"]} completed in {duration}s — result: {result}')

    except Exception as e:
        task["retries"] += 1

        if task["retries"] <= task["max_retries"]:
            delay = 2 ** task["retries"]
            print(f'[WORKER-{worker_id}] Task {task["id"]} FAILED ({e}) — retry {task["retries"]}/3 in {delay}s')

            time.sleep(delay)
            r.lpush(QUEUE, json.dumps(task))
        else:
            task["status"] = "DEAD"

            r.lpush(DEAD, json.dumps(task))
            r.hset(RESULT, task["id"], json.dumps({
                "func": func_name,
                "status": "DEAD",
                "retries": task["retries"],
                "duration": "-"
            }))

            print(f'[WORKER-{worker_id}] Task {task["id"]} moved to DEAD LETTER')


def start_worker(worker_id):
    print(f"[WORKER-{worker_id}] Started")

    while True:
        _, data = r.brpop(QUEUE)
        task = json.loads(data)
        execute_task(task, worker_id)


if __name__ == "__main__":
    import sys
    wid = sys.argv[1] if len(sys.argv) > 1 else "1"
    start_worker(wid)