from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379"
    alpaca_api_key: str
    alpaca_api_secret: str

    class Config:
        env_file = ".env"


settings = Settings()
