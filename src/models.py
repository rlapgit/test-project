from datetime import datetime

from sqlalchemy import JSON, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	pass


class Message(Base):
	"""Таблица для хранения сообщений"""
	__tablename__ = "messages"

	id: Mapped[int] = mapped_column(primary_key=True)
	payload: Mapped[dict] = mapped_column(
		JSON,
		nullable=False,
	)
	received_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
	)
	processed_at: Mapped[datetime | None] = mapped_column(
		DateTime(timezone=True),
		nullable=True,
	)
