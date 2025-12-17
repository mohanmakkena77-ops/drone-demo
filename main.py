from fastapi import FastAPI
import redis

app = FastAPI()

# Connect to Redis
# host="redis" matches the service name in docker-compose.yml
r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/")
def read_root():
    # Increment the counter in Redis
    count = r.incr("hits")
    return {"message": "Hello! You have visited this page", "count": count}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "status": "In Stock"}