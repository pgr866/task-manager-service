# worker/worker.py
import os
import pika
import json
import time

def main():
    rabbitmq_url = os.environ.get('RABBITMQ_URL')
    connection = None
    # Bucle para reintentar la conexión si RabbitMQ no está listo
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            print("Worker: Conectado a RabbitMQ.", flush=True)
        except pika.exceptions.AMQPConnectionError:
            print("Worker: Esperando a RabbitMQ...", flush=True)
            time.sleep(5)
    channel = connection.channel()
    channel.queue_declare(queue='task_created', durable=True, arguments={'x-dead-letter-exchange': 'task_created_dlx'})
    channel.queue_declare(queue='task_completed', durable=True)

    def callback(ch, method, properties, body):
        task_data = json.loads(body)
        if 'body' in task_data:
            task_data = task_data['body']
        if 'title' not in task_data:
            print(f"[Worker] Mensaje malformado: {task_data}, rechazando...", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Va a DLX
            return
        print(f" [x] Recibido y procesado nuevo task: ID={task_data.get('id')}, Título='{task_data.get('title')}'", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_task_completed(ch, method, properties, body):
        task_data = json.loads(body)
        print(f" [+] Tarea completada: ID={task_data.get('id')}, Título='{task_data.get('title')}'", flush=True)
        # Aquí iría la lógica de procesamiento (enviar notificación, etc.)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_created', on_message_callback=callback)
    # channel.basic_consume(queue='task_completed', on_message_callback=callback_task_completed)
    print(' [*] Esperando mensajes. Para salir presione CTRL+C', flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido', flush=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)