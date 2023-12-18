import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SMTP_EMAIL_PASSWORD = os.getenv('SMTP_EMAIL_PASSWORD')
    SMTP_EMAIL_ADDRESS = os.getenv('SMTP_EMAIL_ADDRESS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))) or timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))) or timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    BASE_URL = os.getenv('BASE_URL', os.path.dirname(__file__))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
