FROM python:3.12-slim-bullseye

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

ENV PYTHONPATH "${PYTHONPATH}:/src"

ENTRYPOINT ["python", "src/main.py"]
