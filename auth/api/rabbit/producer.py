import pika
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from conf.config import RABBIT_URL


def publish_message(queue_name: str, message: str):
    params = pika.URLParameters(RABBIT_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message.encode(),
        properties=pika.BasicProperties(delivery_mode=2)  # Сообщение сохраняется при перезапуске
    )

    connection.close()

