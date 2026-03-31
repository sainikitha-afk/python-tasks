from fastapi import FastAPI, Request
import aiohttp
import time

app = FastAPI()

# -----------------------------
# CONFIG
# -----------------------------
ROUTES = {
    "/api/users": "http://localhost:3001",
    "/api/orders": "http://localhost:3001",
    "/api/products": "http://localhost:3001",
}

RATE_LIMIT = 50  # requests per minute
TOKENS = {}
LAST_REFILL = {}

CACHE = {}
CACHE_TTL = 60

CIRCUIT = {
    "failures": 0,
    "open": False,
    "last_failed": 0
}

# -----------------------------
# TOKEN BUCKET
# -----------------------------
def allow_request(api_key):
    now = time.time()

    if api_key not in TOKENS:
        TOKENS[api_key] = RATE_LIMIT
        LAST_REFILL[api_key] = now

    elapsed = now - LAST_REFILL[api_key]

    refill = int(elapsed * (RATE_LIMIT / 60))
    TOKENS[api_key] = min(RATE_LIMIT, TOKENS[api_key] + refill)
    LAST_REFILL[api_key] = now

    if TOKENS[api_key] > 0:
        TOKENS[api_key] -= 1
        return True

    return False

# -----------------------------
# CACHE
# -----------------------------
def get_cache(key):
    if key in CACHE:
        data, expiry = CACHE[key]
        if time.time() < expiry:
            return data
    return None

def set_cache(key, value):
    CACHE[key] = (value, time.time() + CACHE_TTL)

# -----------------------------
# CIRCUIT BREAKER
# -----------------------------
def circuit_open():
    if CIRCUIT["open"]:
        if time.time() - CIRCUIT["last_failed"] > 30:
            CIRCUIT["open"] = False
            CIRCUIT["failures"] = 0
        return CIRCUIT["open"]
    return False

# -----------------------------
# ROUTER
# -----------------------------
@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST"])
async def gateway(service: str, path: str, request: Request):

    api_key = request.headers.get("x-api-key", "anonymous")

    # RATE LIMIT
    if not allow_request(api_key):
        print(f"[REQ] RATE LIMITED ({api_key})")
        return {"error": "Too many requests"}, 429

    full_path = f"/{service}/{path}"
    target = ROUTES.get(f"/api/{service}")

    url = target + full_path

    # CACHE (GET only)
    if request.method == "GET":
        cached = get_cache(url)
        if cached:
            print(f"[REQ] {url} -> CACHE HIT")
            return cached

    # CIRCUIT BREAKER
    if circuit_open():
        print(f"[REQ] {url} -> CIRCUIT OPEN")
        return {"error": "Service unavailable"}, 503

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

                # simulate failure detection
                if "error" in data:
                    raise Exception("Service failed")

                set_cache(url, data)

                print(f"[REQ] {url} -> PROXY SUCCESS")
                return data

    except:
        CIRCUIT["failures"] += 1
        CIRCUIT["last_failed"] = time.time()

        if CIRCUIT["failures"] >= 5:
            CIRCUIT["open"] = True

        print(f"[REQ] {url} -> FAILURE ({CIRCUIT['failures']})")
        return {"error": "Service failure"}, 500