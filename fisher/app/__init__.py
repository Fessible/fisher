from flask import Flask


def create_app():
    app = Flask(__name__)
    # import config
    # 也可以使用from_object(config)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
