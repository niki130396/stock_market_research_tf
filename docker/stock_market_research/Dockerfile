FROM python:3.12-slim-bullseye

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

RUN pip install numpy==1.26.4

RUN --mount=type=secret,id=STOCK_MARKET_RESEARCH_DB_USER_PASSWORD \
    mkdir ./some_dir \
    && echo "$(cat /run/secrets/STOCK_MARKET_RESEARCH_DB_USER_PASSWORD)" >> ./some_dir/db_password.txt

RUN --mount=type=secret,id=SOME_SECRET \
    echo "$(cat /run/secrets/SOME_SECRET)" >> ./some_dir/random_stuff.txt \

ENV SOME_SECRET="$(cat ./some_dir/random_stuff.txt)"

ENV STOCK_MARKET_RESEARCH_DB_USER_PASSWORD="$(cat ./some_dir/db_password.txt)"

WORKDIR src

CMD ["python", "main.py"]
##
