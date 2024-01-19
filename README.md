# tradingview-interactivebroker
TradingView Webhook and Interactive Broker Python Integration
=======

### Port Settings
Paper Trading : 7497
Live Trading : 7496

## FastAPI Port
9081

## Instructions to Run the Program
### Source Code
Note: Using docker container for redis-stack
1. Run the redis-stack docker container
2. Activate virtual envirnoment
3. run the command : py src\main.py
4. For dashbaord of orders, open browser and type http://127.0.0.1:9081/

# Docker Images
## IB Gateway Docker
docker build -t ib-gateway -f ./build/ibgw.Dockerfile .
docker build -t ib-gateway-alpine .
docker run -p 7497:7497 -p 7496:7496 --name ib-gateway-container-alpine ib-gateway-alpine

## NGINX Docker

docker build -t nginx-server -f ./build/nginx.Dockerfile .
docker run -d -p 80:80 --link tv-webhook:tv-webhook --name nginx-server nginx-server

## TradingView Webhook Docker
docker build -t tv-webhook .
docker run -d -p 9081:9081 --name tv-webhook tv-webhook

# Desktop Manual Docker Run

1 Start Redis  and bind port
2 Start ib-gateway and bing ports, provide the environment varialbles such as username, password, papertraing, apireadonly = no
3 activate the python environment
4.navigate to project directory and type py src\main.py
5. For dashboard , In browser enter :http://127.0.0.1:9081/ 
6. For APIs , In browser enter :http://127.0.0.1:9081/docs



