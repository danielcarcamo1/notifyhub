from flask import Flask, request, jsonify
import pika
import os

app = Flask(__name__)

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBITMQ_USER", "rmq_user")
RABBIT_PASS = os.getenv("RABBITMQ_PASS", "rmq_pass")
INSTANCE_ID = os.getenv("INSTANCE_ID", "api-x")

def publish_message(queue, body):
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=body)
    connection.close()

@app.route("/api/v1/notifications/email", methods=["POST"])
def send_email():
    data = request.json
    publish_message("q.email", str({"instance": INSTANCE_ID, **data}))
    return jsonify({"status": "accepted"}), 202

@app.route("/api/v1/notifications/sms", methods=["POST"])
def send_sms():
    data = request.json
    publish_message("q.sms", str({"instance": INSTANCE_ID, **data}))
    return jsonify({"status": "accepted"}), 202

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "instance": INSTANCE_ID})

app.run(host="0.0.0.0", port=5000)


