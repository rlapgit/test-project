from pydantic import BaseModel


class MetadataSchema(BaseModel):
	"""Метаданные входящего сообщения"""
	timestamp: int


class MessageSchema(BaseModel):
	"""Схема входящего сообщения"""
	data: dict
	metadata: MetadataSchema
