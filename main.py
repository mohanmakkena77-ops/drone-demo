from fastapi import FastAPI, Request
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

@app.post("/hook")
async def github_webhook(request: Request):
    try:
        headers = dict(request.headers)
        print(f"Headers: {headers}")
        
        body = await request.json()
        print(f"Body received: {type(body)}")
        
        event_type = headers.get("x-github-event")
        delivery_id = headers.get("x-github-delivery")
        
        print(f"Received GitHub {event_type} event: {delivery_id}")
        
        if event_type == "push":
            repo_name = body.get("repository", {}).get("name")
            pusher = body.get("pusher", {}).get("name")
            commits = len(body.get("commits", []))
            print(f"Push to {repo_name} by {pusher} with {commits} commits")
        
        return {"status": "received", "event": event_type}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"error": str(e)}, 500