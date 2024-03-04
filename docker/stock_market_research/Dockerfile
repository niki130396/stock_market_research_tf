FROM python:3.12-slim-bullseye

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

WORKDIR src

RUN --mount=type=secret,id=STOCK_MARKET_RESEARCH_DB_USER_PASSWORD \
    STOCK_MARKET_RESEARCH_DB_USER_PASSWORD="$(cat /run/secrets/STOCK_MARKET_RESEARCH_DB_USER_PASSWORD)" \
    && export STOCK_MARKET_RESEARCH_DB_USER_PASSWORD

CMD ["python", "main.py"]
##
