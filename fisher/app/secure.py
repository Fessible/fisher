import os


# 数据库密码账号等机密信息，不上传到git上面
DEBUG = False

# 数据库配置

DIALECT = 'mysql'
USER = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
DATABASE = 'fisher'

SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}'.format(DIALECT, USER, PASSWORD, HOST, DATABASE)

# SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/flask_sql_demo'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SECRET_KEY = os.urandom(24)