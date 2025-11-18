FROM python:3.10-slim

WORKDIR /app

COPY worker.py /app/

RUN pip install pika mysql-connector-python

CMD ["python", "worker.py"]