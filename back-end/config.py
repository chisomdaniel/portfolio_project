import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)

class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG', True)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///dev_database.db')

class ProductionConfig(Config):
    DEBUG = os.environ.get('DEBUG', False)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
