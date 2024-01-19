FROM python:3.12.1-alpine3.19

RUN echo 'Running Docker Build for TradingView Interactive Broker WebHook Integration'

WORKDIR /app
COPY ./src /app/src
COPY ./templates /app/templates
COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install -r ./requirements.txt --upgrade --no-cache-dir

# EXPOSE map[9081/tcp:{}]
# EXPOSE 9081
EXPOSE 80

# EXPOSE 6379 7497 7496 9081

CMD ["python", "src/main.py"]