from . import web
from app.forms.book import SearchForm
from flask import request, flash, jsonify, json

from app.view_models.book import BookCollection
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook


@web.route('/book/search')
def search():
    """
           q :普通关键字 isbn
           ?q=金庸&page=1
    """
    # 获取请求内容
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data

        # 判断是否为isbn
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        # 搜索结果，并存储到yushu_book中
        if isbn_or_key:
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_key(q, page)

        # 封装数据
        books.fill(yushu_book, q)

    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        return jsonify(form.errors)

    # 由于books是对象，需要将对象转换成json
    return json.dumps(books, default=lambda o: o.__dict__)
