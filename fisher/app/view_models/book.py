# 输出格式

class BookViewModel:
    """
    {
    "author": [
        "蔡智恒"
    ],
    "binding": "平装",
    "category": "小说",
    "id": 1780,
    "image": "https://img3.doubanio.com/lpic/s1327750.jpg",
    "images": {
        "large": "https://img3.doubanio.com/lpic/s1327750.jpg"
    },
    "isbn": "9787501524044",
    "pages": "224",
    "price": "12.80",
    "pubdate": "1999-11-1",
    "publisher": "知识出版社",
    "subtitle": "",
    "summary": "你还没有试过，到大学路的麦当劳，点一杯大可乐，与两份薯条的约会方法吗？那你一定要读目前最抢手的这部网络小说——《第一次的亲密接触》。\\n由于这部小说在网络上一再被转载，使得痞子蔡的知名度像一股热浪在网络上延烧开来，达到无国界之境。作者的电子信箱，每天都收到热情的网友如雪片飞来的信件，痞子蔡与轻舞飞扬已成为网络史上最发烧的网络情人。",
    "title": "第一次的亲密接触",
    "translator": []
}
    """

    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author = '、'.join(book['author'])
        self.summary = book['summary']
        self.image = book['image']
        self.isbn = book['isbn']
        self.price = book['price']

    # 希望输出 author/publisher/price 或者 author/price的格式
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    """
     YuShuBook:
        total,
        books
    """

    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, data, keyword):
        self.total = data.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in data.books]
