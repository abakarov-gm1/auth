import pika
from controllers.decode_access_token import decode_access_token_new
from producer import publish_message

RABBITMQ_HOST = "rabbitmq"  # Или "localhost", если не в Docker
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"
QUEUE_NAME = "get_user"

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)


def callback(ch, method, properties, body):
    if method.routing_key == "get_user":
        token = body.decode()
        payload = decode_access_token_new(token)
        publish_message(queue_name="get_user_response", message=payload)
        pass


channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)


print("Ожидание сообщений. Для выхода нажми CTRL+C")
channel.start_consuming()
