import redis, sqlite3, time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

r = redis.Redis(host='localhost', port=6379, db=0)

conn = sqlite3.connect('trade.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        ticker,
        order_action,
        order_contracts,
        order_price
    )
""")
conn.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('trade.db')
        g.db.row_factory = sqlite3.Row

    return g.db

@app.get('/')
def dashboard(response_class=HTMLResponse):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM signals
    """)
    signals = cursor.fetchall()
    return templates.TemplateResponse(name='dashboard.html', context={"signals": signals}
    )


@app.route('/status')
def index():
    return {'hello': 'world'}


@app.route("/placeOrder", methods=['POST'])
def ib_place_order():
    print("Received Order From TradingView")
    webhook_msg = app.current_request.json_body
    print(f"Order Request Received for : {webhook_msg}")
    if webhook_msg:
        r.publish('tradingview', webhook_msg)

        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO signals (ticker, order_action, order_contracts, order_price) 
            VALUES (?, ?, ?, ?)
        """, (webhook_msg['ticker'], 
                webhook_msg['strategy']['order_action'], 
                webhook_msg['strategy']['order_contracts'],
                webhook_msg['strategy']['order_price']))

        db.commit()

        return webhook_msg

    return {
        "code": "success"
    }

@app.route("/getTicker", methods=['GET'])
def get_ticker():
    return {"TICKER": "MSFT"}



# {
#     "TimeStamp": "2023-12-01T20:55:10Z",
#     "Curreny": "USD",
#     "Exchange": "BATS",
#     "Ticker": "AAPL",
#     "Price": 191.09,
#     "Volume": 23330
# }