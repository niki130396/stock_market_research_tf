FROM python:3.12-slim-bullseye

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

RUN --mount=type=secret,id=STOCK_MARKET_RESEARCH_DB_USER_PASSWORD \
    echo "$(cat /run/secrets/STOCK_MARKET_RESEARCH_DB_USER_PASSWORD)" >> $HOME/db_password.txt

ENV STOCK_MARKET_RESEARCH_DB_USER_PASSWORD="$(cat $HOME/db_password.txt)"

WORKDIR src

CMD ["python", "main.py"]
##
