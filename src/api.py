import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from redis_client import redis_client

app = FastAPI()

# Get the directory of the current script
parent_dir = os.path.abspath(os.path.curdir)
# Construct the path to the "templates" folder
templates_folder = os.path.join(parent_dir, "templates")
print(f"templates folder : {templates_folder}")

templates = Jinja2Templates(directory=templates_folder)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    orders = redis_client.get_all_orders()
    return templates.TemplateResponse('dashboard.html', {"request": request, "orders": orders})

@app.get('/status')
def index():
    return {'hello': 'world'}

@app.post("/placeOrder")
async def ib_place_order(request: Request, webhook_msg: dict):
    try:
        print("Received Order From TradingView")
        # Check if the request has JSON content
        if request.headers.get("content-type") == "application/json":
            # Parse the JSON payload
            webhook_msg = await request.json()
            print(f"Order Request Received for : {webhook_msg}")
            wb_msg_str = json.dumps(webhook_msg)
            redis_client.publish_message(wb_msg_str)
            redis_client.write_db(webhook_msg)
            return {"message": "JSON data received successfully", "data": webhook_msg}
        elif request.headers.get("content-type") == "plain/text":
            pass
        else:
            raise HTTPException(
                status_code=400, detail="Invalid content type. Expected 'application/json'.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error decoding webhook message: {str(e)}")