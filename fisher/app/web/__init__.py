from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import book, auth, drift, gift, main, wish

from app.web import book

@web.context_processor
def context_processor():
    return {'current_user': 'zhangsan'}
