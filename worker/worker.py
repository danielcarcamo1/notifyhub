import pika
import mysql.connector
import os
import time

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBITMQ_USER", "rmq_user")
RABBIT_PASS = os.getenv("RABBITMQ_PASS", "rmq_pass")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_DB = os.getenv("MYSQL_DB", "notifyhub")
MYSQL_USER = os.getenv("MYSQL_USER", "nh_user")
MYSQL_PASS = os.getenv("MYSQL_PASS", "nh_pass")

def save_log(worker_id, queue, payload):
    db = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, database=MYSQL_DB
    )
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO logs (worker, cola, payload) VALUES (%s, %s, %s)",
        (worker_id, queue, payload)
    )
    db.commit()
    cursor.close()
    db.close()

def callback(ch, method, properties, body):
    print(f"[x] Mensaje recibido en {method.routing_key}: {body.decode()}")
    save_log("worker-1", method.routing_key, body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

def connect_rabbit():
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
    for intento in range(1, 11):
        try:
            print(f"Intentando conectar a RabbitMQ (intento {intento}/10)...")
            conn = pika.BlockingConnection(params)
            print("✅ Conectado a RabbitMQ")
            return conn
        except Exception as e:
            print(f"❌ No se pudo conectar a RabbitMQ: {e}")
            time.sleep(5)
    print("❌ No se logró conectar a RabbitMQ después de varios intentos. Saliendo.")
    raise SystemExit(1)

connection = connect_rabbit()
channel = connection.channel()

for q in ["q.email", "q.sms"]:
    channel.queue_declare(queue=q)
    channel.basic_consume(queue=q, on_message_callback=callback)

print("Worker escuchando colas q.email y q.sms...")
channel.start_consuming()