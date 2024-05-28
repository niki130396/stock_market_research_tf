FROM python:3.12-slim-bullseye

COPY requirements/stock_market_research_workloads.txt requirements.txt

RUN pip install -r requirements.txt

COPY stock_market_research_workloads stock_market_research_workloads

ENV PYTHONPATH "${PYTHONPATH}:/stock_market_research_workloads"

ENTRYPOINT ["python", "stock_market_research_workloads/main.py"]
