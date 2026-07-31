import json
import logging
from datetime import datetime, timezone

import pika.channel
from pydantic import ValidationError

from config import settings
from db import create_database, save_message
from health import start_health_check
from rabbitmq import start_consuming
from schemas import MessageSchema

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def process_message(body: bytes) -> None:
	"""Сериализировать и сохранить сообщение"""
	raw = json.loads(body)
	message = MessageSchema.model_validate(raw)
	processed_at = datetime.now(timezone.utc)

	payload = {
		"data": message.data,
		"metadata": message.metadata.model_dump(),
	}

	save_message(
		payload=payload,
		processed_at=processed_at,
	)


def on_message(
	channel: pika.channel.Channel,
	method: pika.spec.Basic.Deliver,
	properties: pika.spec.BasicProperties,
	body: bytes,
) -> None:
	"""Обработать входящее сообщение из RabbitMQ"""
	logger.info("Получено новое сообщение")

	try:
		# Обрабатываем, валидируем и сохраняем сообщение
		process_message(body)

		# Подтверждаем получение сообщения
		channel.basic_ack(
			delivery_tag=method.delivery_tag,
		)

		logger.info("Сообщение успешно обработано")

	except (json.JSONDecodeError, ValidationError) as error:
		# Отклоняем сообщение некорректного формата
		logger.error(f"Некорректное сообщение: {error}")

		# Отклонить сообщение без повтора
		channel.basic_reject(
			delivery_tag=method.delivery_tag,
			requeue=False,
		)

	except Exception as error:
		# Отправить сообщение на повторную обработку
		logger.error(f"Ошибка обработки: {error}")
		headers = properties.headers or {}
		retry_count = headers.get("x-retry-count", 0)

		if retry_count >= settings.RETRY_COUNT:
			logger.exception("Превышено количество попыток")

			# Исчерпаны попытки, отклоняем сообщение
			channel.basic_reject(
				delivery_tag=method.delivery_tag,
				requeue=False,
			)
			return

		logger.warning(f"Повторная попытка {retry_count + 1}/{settings.RETRY_COUNT}")

		# Отправить сообщение на повторную обработку
		channel.basic_publish(
			exchange="",
			routing_key=settings.RABBITMQ_QUEUE,
			body=body,
			properties=pika.BasicProperties(
				headers={
					**headers,
					"x-retry-count": retry_count + 1,
				},
				delivery_mode=2,
				content_type="application/json",
			),
		)

		# Удалить старое сообщение из очереди
		channel.basic_ack(
			delivery_tag=method.delivery_tag,
		)


if __name__ == "__main__":
	logger.info("Запуск сервиса")
	create_database()
	start_health_check()
	logger.info("Ожидание сообщений из RabbitMQ")
	start_consuming(on_message)
