import os
from datetime import timedelta

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'todo'
USENAME = 'root'
PASSWORD = 'puhao'
DB_URI = "mysql://{}:{}@{}:{}/{}?charset=utf8".format(USENAME, PASSWORD, HOSTNAME, PORT, DATABASE)
PAGE_SIZE = 9
USER_ID="app_user_id"

class BaseConfig(object):
    SECRET_KEY=os.urandom(24)
    #SECRET_KEY = 'puxiaoshuai20181212'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME= timedelta(hours=5)



class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
