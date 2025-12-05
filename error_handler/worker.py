import pika
import json
import os

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@mq:5672/")

connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Declaramos la cola de Dead Letters
channel.queue_declare(queue='tasks_failed', durable=True)

def callback(ch, method, properties, body):
    msg = json.loads(body)
    # Guardar en log
    with open("/logs/failed_tasks.log", "a") as f:
        f.write(json.dumps(msg) + "\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Mensaje fallido registrado: {msg}", flush=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='tasks_failed', on_message_callback=callback)

print("[ErrorHandler] Esperando mensajes en tasks_failed...", flush=True)
channel.start_consuming()