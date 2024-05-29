FROM python:3.12-slim-bullseye

COPY requirements/stock_market_research_dashboard.txt requirements.txt

RUN pip install -r requirements.txt

COPY stock_market_research_dashboard stock_market_research_dashboard

ENV PYTHONPATH "${PYTHONPATH}:/stock_market_research_dashboard"

EXPOSE 8050

ENTRYPOINT ["python", "stock_market_research_dashboard/app.py"]
