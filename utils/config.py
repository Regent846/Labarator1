import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс для управления конфигурацией приложения."""

    BASE_URL = os.getenv('BASE_URL', 'https://jsonplaceholder.typicode.com')
    ENV = os.getenv('ENV', 'dev')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    TIMEOUT = int(os.getenv('TIMEOUT', '10'))

    @classmethod
    def get_base_url(cls):
        return cls.BASE_URL

    @classmethod
    def get_environment(cls):
        return cls.ENV