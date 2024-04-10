import os

admins = [6045160449]


class Settings:
    POSTGRES_SERVICE = os.getenv('POSTGRES_SERVICE')
    POSTGRES_NAME = os.getenv('POSTGRES_NAME')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')


settings = Settings()
