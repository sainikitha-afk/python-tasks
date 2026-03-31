import json

WAL_FILE = "wal.log"

def log(entry):
    with open(WAL_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def load_logs():
    try:
        with open(WAL_FILE, "r") as f:
            return [json.loads(line) for line in f]
    except FileNotFoundError:
        return []