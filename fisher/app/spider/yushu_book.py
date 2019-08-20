# 发送请求获取数据

# 通过这个获取到当前的app，从而获取配置文件做的内容
from flask import current_app

from app.libs.httper import HTTP


class YuShuBook:
    # 查询地址
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        # 存储数据
        self.__file_single(result)

    def search_by_key(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.get_start_page(page))
        result = HTTP.get(url)
        self.__file_collection(result)

    def get_start_page(self, page):
        # page从0开始,0,10,20
        return (page - 1) * current_app.config['PER_PAGE']

    # 存储单个数据
    def __file_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    # 存储数据集合
    def __file_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    # 获取第一个，查询结果为books[{},{}]
    def first(self):
        return self.books[0] if self.total >= 1 else None
