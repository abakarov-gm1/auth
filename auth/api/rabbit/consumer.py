import sys
import os
import pika
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controllers.decode_access_token import decode_access_token_new
from repositories.user_repository import get_user_service


RABBITMQ_HOST = "rabbitmq"  # Или "localhost", если не в Docker
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

with pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)) as connection:
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')


    def on_request(ch, method, props, body):
        token = body.decode()
        user = get_user_service(token)
        if user:
            user_dict = {key: value for key, value in user.__dict__.items() if not key.startswith("_")}
            user_json = json.dumps(user_dict)
        else:
            user_json = json.dumps({"error": "User not found"})

        print("Отправляем JSON:", user_json)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=user_json
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)


    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print(" Консюмер начал слушать:")
    channel.start_consuming()
