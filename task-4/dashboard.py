import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

RESULT = "results"

print("\n=== Dashboard ===")
print("+----------+--------+-----------+--------+-------------+")
print("| Task ID  | Func   | Status    | Retries| Duration    |")
print("+----------+--------+-----------+--------+-------------+")

for tid, data in r.hgetall(RESULT).items():
    d = json.loads(data)

    print(f"| {tid:<8} | {d['func'][:6]:<6} | {d['status']:<9} | {d['retries']:<6} | {d['duration']:<11} |")

print("+----------+--------+-----------+--------+-------------+")