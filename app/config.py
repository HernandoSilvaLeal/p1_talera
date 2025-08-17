from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    service_name: str = "order-service"
    mongo_uri: str = "mongodb://localhost:27017/orders"
    log_level: str = "INFO"
    idempotency_ttl_seconds: int = 86400

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
