import uvicorn
import asyncio
import redis
import time
import json
import threading
import signal


from fastapi import FastAPI
from api import app
from ib_handler import ib_client
from redis_client import redis_client

def check_messages():
    while True:
        print(f"{time.time()} - checking for tradingview webhook messages")
        order_msg = redis_client.get_message()
        if order_msg is not None and order_msg['type'] == 'message':
            print(f"tradingview webhook messages:{order_msg}")
            order_info = json.loads(order_msg['data'])
            trade = ib_client.execute_order(order_info)
            time.sleep(1)
            ib_client.get_order_status(trade)
     
        time.sleep(1)  # Adjust the sleep duration as needed

# Define a function to run ib.run() in a separate thread
def run_ib():
    ib_client.ib.run()
    # while True:
    #     time.sleep(1)  # Adjust the sleep duration as needed

# Set up a signal handler to stop the loop on Ctrl+C
def signal_handler(signum, frame):
    print(" Received Keyboard Interrupt. Stopping the application....")
    ib_client.close_connection()
    redis_client.close()

def main():

    signal.signal(signal.SIGINT, signal_handler)

    # Test Redis connection
    try:
        redis_client.client.ping()
        print("Successfully connected to Redis.")
    except redis.ConnectionError:
        print("Error connecting to Redis.")


    # Start the check_messages coroutine in a separate thread
    print(" Initiating checking for webhook messages in background thread.")
    check_messages_thread = threading.Thread(target=check_messages, daemon=True)
    check_messages_thread.start()

    # # Start the check_messages coroutine in a separate thread
    # print(" Initiating IB Handler background thread.")
    # ib_thread = threading.Thread(target=run_ib, daemon=True)
    # ib_thread.start()

    print(" Running the main application.")
    # uvicorn.run(app, host="127.0.0.1", port=9081)
    uvicorn.run(app, host="tv-webhook", port=80)


if __name__ == "__main__":
    main()


