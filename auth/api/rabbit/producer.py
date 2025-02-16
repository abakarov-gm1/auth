
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from controllers.decode_access_token import decode_access_token_new
#
# RABBITMQ_HOST = "rabbitmq"  # Или "localhost", если не в Docker
# RABBITMQ_USER = "user"
# RABBITMQ_PASS = "password"
# import pika
#
# # Подключаемся к RabbitMQ
# credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
# channel = connection.channel()
#
# # Имя очереди
# queue_name = 'rpc_queue'
#
# # Получаем одно сообщение (без удаления)
# method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=False)
#
#
# print(method_frame)
# print(header_frame)
# print(body)
#
# # if method_frame:
# #     print(f"Сообщение: {body.decode()}")
# # else:
# #     print("Очередь пуста")
#
#
# connection.close()



