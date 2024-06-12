FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y \
    curl

# Install google cloud sdk
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-463.0.0-linux-x86_64.tar.gz
RUN tar -xf google-cloud-cli-463.0.0-linux-x86_64.tar.gz \
    && ./google-cloud-sdk/install.sh
ENV PATH="./google-cloud-sdk/bin:$PATH"

RUN --mount=type=secret,id=STOCK_MARKET_RESEARCH_USER_SA_KEY \
    mkdir ./google \
    && echo "$(cat /run/secrets/STOCK_MARKET_RESEARCH_USER_SA_KEY)" | base64 -d >> ./google/service_account.json

ENV GOOGLE_APPLICATION_CREDENTIALS="/google/service_account.json"

COPY requirements/stock_market_research_dashboard.txt requirements.txt

RUN pip install -r requirements.txt

COPY stock_market_research_dashboard stock_market_research_dashboard
COPY utils stock_market_research_dashboard/utils

ENV PYTHONPATH "${PYTHONPATH}:/stock_market_research_dashboard"

EXPOSE 8050

WORKDIR stock_market_research_dashboard

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
