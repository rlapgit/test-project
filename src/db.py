from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base, Message

engine = create_engine(
	settings.database_url,
	echo=False,
)

SessionLocal = sessionmaker(
	bind=engine,
	autoflush=False,
	autocommit=False,
)


def create_database() -> None:
	"""Создать таблицы в базе данных"""
	Base.metadata.create_all(bind=engine)


def save_message(
	payload: dict,
	processed_at: datetime,
) -> None:
	"""Сохранить сообщение в базу данных"""
	with SessionLocal() as session:
		try:
			message = Message(
				payload=payload,
				processed_at=processed_at,
			)
			session.add(message)
			session.commit()
		except:
			session.rollback()
			raise
