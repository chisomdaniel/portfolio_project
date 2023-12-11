import os

class Config:
    SECRET_KEY = 'wgwf24gfefgrgw34eg5y346g5yge'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_dev_database.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Replace with your production database URL

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
