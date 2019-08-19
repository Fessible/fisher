from flask import Flask
from  app.models.base import db

def create_app():
    app = Flask(__name__)
    # import config
    # 也可以使用from_object(config)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    #数据库初始化
    db.init_app(app)
    with app.app_context():
        db.create_all()


    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
