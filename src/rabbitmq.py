import pika
import pika.channel

from config import settings


def create_connection() -> pika.BlockingConnection:
	"""Создать подключение к RabbitMQ"""
	credentials = pika.PlainCredentials(
		username=settings.RABBITMQ_USER,
		password=settings.RABBITMQ_PASS,
	)

	parameters = pika.ConnectionParameters(
		host=settings.RABBITMQ_HOST,
		port=settings.RABBITMQ_PORT,
		credentials=credentials,
	)

	return pika.BlockingConnection(parameters)


def start_consuming(on_message) -> None:
	"""Начать прослушивание очереди RabbitMQ"""
	connection = create_connection()

	channel = connection.channel()

	# Подключиться к очереди
	channel.queue_declare(
		queue=settings.RABBITMQ_QUEUE,
		durable=True,
	)

	# Читать сообщения по одному
	channel.basic_qos(prefetch_count=1)

	# Регистрируем обработчик сообщений
	channel.basic_consume(
		queue=settings.RABBITMQ_QUEUE,
		on_message_callback=on_message,
	)

	# Ожидаем новое сообщение
	channel.start_consuming()
