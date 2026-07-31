from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	# RabbitMQ
	RABBITMQ_HOST: str
	RABBITMQ_PORT: int
	RABBITMQ_USER: str
	RABBITMQ_PASS: str
	RABBITMQ_QUEUE: str

	# PostgreSQL
	POSTGRES_HOST: str
	POSTGRES_PORT: int
	POSTGRES_USER: str
	POSTGRES_PASS: str
	POSTGRES_DB: str
	POSTGRES_TABLE: str  # ?

	# Logs
	LOG_LEVEL: str = "INFO"

	# Retry
	RETRY_COUNT: int = 3

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)

	@property
	def database_url(self) -> str:
		return (
			f"postgresql+psycopg2://"
			f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}"
			f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
			f"/{self.POSTGRES_DB}"
		)


settings = Settings()
