import os
import sys
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible 判断系统环境
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # MAIL_SERVER = os.getenv('MAIL_SERVER')  # 服务器
    # MAIL_PORT = 465  # 端口 ssl 456 tls 587 默认 25
    # MAIL_USE_TLS = False  # 使用 STARTTLS 只能选择一个
    # MAIL_USE_SSL = True  # 使用ssl/tls
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)  # 发信人

    CELERY_BROKER_URL = 'redis://:redis@localhost:6379',
    CELERY_RESULT_BACKEND = 'redis://:redis@localhost:6379'

    CELERYBEAT_SCHEDULE = {
        # ＃ 定义任务名称：import_data
        # ＃ 执行规则：每10秒运行一次
        'import_data': {
            'task': 'import_data',
            'schedule': timedelta(seconds=5)
        },
    }

class DevelopmentConfig(BaseConfig):
    pass
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))

config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}
