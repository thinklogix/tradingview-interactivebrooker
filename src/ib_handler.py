from ib_insync import IB, Stock, MarketOrder
from ib_insync import *

class InteractiveBrokersHandler:
    def __init__(self):
        print(" Initializing Interactive Brokers Handler")
        util.startLoop()
        self.ib = IB()
        # self.ib.connect('127.0.0.1', 4002, clientId=1)
        # self.ib.connect('localhost', 4002, clientId=1)
        self.ib.connect('ib-gateway',4002, clientId=1)
        if self.ib.isConnected():
            print(" Established connection to IB-Gateway...")
        else:
            print(" Having trouble in connecting to IB-Gateway...")
        

    def execute_order(self, order_info):
        print(" Executing order... ")
        symbol = order_info['ticker']
        exchange = order_info['exchange']
        action = order_info['strategy']['order_action']
        totalQuantity = order_info['strategy']['order_contracts']
        stock = Stock(symbol, 'SMART', 'USD', primaryExchange=exchange)
        order = MarketOrder(action, totalQuantity)
        trade = self.ib.placeOrder(stock, order)
        return trade
    
    def get_order_status(self, trade):
        print(" Getting Order Status .....")
        print(trade.log)


    def close_connection(self):
        print(" Closing Interactive Brokers Handler Connection...")
        if self.ib.isConnected():
            self.ib.disconnect()


ib_client = InteractiveBrokersHandler()
# ib_client.ib.run()