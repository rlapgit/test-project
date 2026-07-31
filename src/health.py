import logging
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from rabbitmq import create_connection

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
def health_check():
	"""Проверить состояние сервиса"""
	# По тз непонятно, пусть мониторится состояние RabbitMQ
	try:
		connection = create_connection()
		connection.close()
		return {"status": "ok"}

	except Exception:
		return JSONResponse(
			status_code=503,
			content={"status": "error"},
		)


def start_health_check():
	"""Запустить сервер для мониторинга состояния"""
	thread = threading.Thread(
		target=uvicorn.run,
		kwargs={
			"app": app,
			"host": "0.0.0.0",
			"port": 8000,
		},
		daemon=True,
	)
	thread.start()

	logger.info("Мониторинг состояния запущен")
