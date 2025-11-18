FROM python:3.10-slim

WORKDIR /app

COPY app.py /app/

RUN pip install flask pika mysql-connector-python

EXPOSE 5000

CMD ["python", "app.py"]