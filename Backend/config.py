import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENV = 'prod'

    if ENV == 'dev':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    SECURITY_PASSWORD_SALT =  os.environ.get('SECURITY_PASSWORD_SALT')
    MAIL_SERVER =  os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME =  os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD =  os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'from@example.com'
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_TIMEOUT = 3000
    SQLALCHEMY_POOL_RECYCLE = 3600 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'