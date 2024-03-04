FROM python:3.11-slim-bullseye

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

CMD ["python", "main.py"]
