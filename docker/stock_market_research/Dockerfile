FROM python:3.12-slim-bullseye

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

RUN pip install numpy==1.26.3

RUN --mount=type=secret,id=STOCK_MARKET_RESEARCH_DB_USER_PASSWORD \
    echo "$(cat /run/secrets/STOCK_MARKET_RESEARCH_DB_USER_PASSWORD)" >> $HOME/db_password.txt

RUN --mount=type=secret,id=SOME_SECRET \
    echo "$(cat /run/secrets/SOME_SECRET)" >> $HOME/random_stuff.txt \

ENV SOME_SECRET="$(cat $HOME/random_stuff.txt)"

ENV STOCK_MARKET_RESEARCH_DB_USER_PASSWORD="$(cat $HOME/db_password.txt)"

WORKDIR src

CMD ["python", "main.py"]
##
