
import redis
import json


class RedisClient:
    def __init__(self, channel:str):
        print(" Initializing Redis Client...")
        self._channel = channel
        # self.client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True) # For running on PC
        # self.client = redis.Redis(host='localhost', port=6379, decode_responses=True) # For running in docker 
        self.client = redis.Redis(host='redis-stack', port=6379, decode_responses=True) # For running in docker as service
        self._sub = self.subscribe_message()

    def publish_message(self, message):
        print(f" Publishing message to redis channel : {message}")
        self.client.publish(self._channel, message)

    def subscribe_message(self):
        print(f" Subscribing to redis channel : {self._channel}")
        redis_sub = self.client.pubsub()
        redis_sub.subscribe(self._channel)
        return redis_sub

    def get_message(self):
        msg = self._sub.get_message()
        return msg

    def write_db(self, order_msg):
        self.client.hset("signals", order_msg['time'], json.dumps(order_msg))

    def get_all_orders(self):
        order_details = []
        orders = self.client.hgetall("signals")
        for timestamp, order in sorted(orders.items(), reverse=True):
            order_dict = json.loads(order)
            # Extract required fields
            data = {
                'time': order_dict['time'],
                'exchange': order_dict['exchange'],
                'ticker': order_dict['ticker'],
                'strategy_name': order_dict['strategy_name'],
                'order_action': order_dict['strategy']['order_action'],
                'order_contracts': order_dict['strategy']['order_contracts'],
                'order_price': order_dict['strategy']['order_price'],
                'market_position': order_dict['strategy']['market_position']
            }
            order_details.append(data)
        return order_details

    def close(self):
        print(" Closing Redis Client Connection...")
        self.client.close()

redis_client = RedisClient('tradingview')
