from . import web


@web.route('/book/search')
def search():
    return 'Hello world!'
