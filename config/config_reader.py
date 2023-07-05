from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    mongo_name: str
    mongo_port: str
    mongo_host: str
    mongo_db: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()