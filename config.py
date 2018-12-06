# import testing.postgresql
# from sqlalchemy import create_engine

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'dev'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@Alex.ngari03@localhost/andelaapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    