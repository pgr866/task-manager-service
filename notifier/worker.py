import os
import pika
import json
import time
import requests

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # URL para simular envío de email

def main():
    rabbitmq_url = os.environ.get('RABBITMQ_URL')
    connection = None
    # Intentos de reconexión si RabbitMQ no está listo
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            print("Notifier: Conectado a RabbitMQ.", flush=True)
        except pika.exceptions.AMQPConnectionError:
            print("Notifier: Esperando a RabbitMQ...", flush=True)
            time.sleep(5)
    channel = connection.channel()
    channel.queue_declare(queue='task_completed', durable=True)

    def callback(ch, method, properties, body):
        task_data = json.loads(body)
        print(f"[Notifier] Tarea completada: ID={task_data.get('id')}, Título='{task_data.get('title')}'", flush=True)
        # Simular envío de email mediante POST al webhook
        try:
            response = requests.post(WEBHOOK_URL, json=task_data)
            print(f"[Notifier] Email simulado enviado, status: {response.status_code}", flush=True)
        except Exception as e:
            print(f"[Notifier] Error al enviar notificación: {e}", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_completed', on_message_callback=callback)
    print(' [*] Esperando mensajes en task_completed. CTRL+C para salir', flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()
