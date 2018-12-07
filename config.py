import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'dev'

    DATABASE_DEFAULT = 'postgresql://postgres:@Alex.ngari03@localhost/andelaapp'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', DATABASE_DEFAULT)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    