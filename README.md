# fisher
鱼书笔记

## 依赖管理工具pipenv
>1. 什么是pipenv?
>2. 为什么要使用pipenv？
>3. 如何使用pipenv？

### 什么是pipenv？
pipenv是Kenneth Reitz在2017年1月发布的Python依赖管理工具，可以看做是pip和virtualenv的组合体，他基于Pipfile的依赖记录方式，而不是requirements.txt的记录方式。

### 为什么使用pipenv？
pipenv会自动帮你管理虚拟环境和依赖文件，并提供了一系列命令和选项来帮助你实现各种依赖和环境管理相关的操作。总之，它更方便，完善，安全。

### 如何使用pipenv？

针对本项目，创建fisher文件夹，进入文件夹后进行如下操作

1. 安装pipenv
```
pip install pipenv
```
2. 创建虚拟环境
```
pipenv install
```
3. 进入虚拟环境
```
pipenv shell
```
4.安装flask
```
pipenv install flask
```


### pipenv安装速度慢怎么解决？
添加镜像，修改pipfile中的url
```
[[source]]
name = "pypi"
#url = "https://pypi.org/simple"
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.7"

```
### 使用pycharm
我们使用pycharm打开项目，根据提示安装pipenv，就完成了环境部署。
查看terminal，结果如下
```
(fisher) Mac-mini:fisher h$
```

## 鱼书项目简介
>1. 鱼书有什么功能？
>2. 涉及哪些方面的知识

### 鱼书有什么功能？

<img src="/images/fisher.png" width="500" hegiht="313" align=center />

目录结构
```
├── app
│   ├── __init__.py 初始化app
│   ├── forms  表单数据
│   ├── libs   工具类
│   ├── models  数据库模型
│   ├── secure.py  存放机密配置，如数据库信息等
│   ├── setting.py 存放一般配置
│   ├── spider  请求API，获取书籍数据，并生成yushuBook类
│   ├── static  静态资源文件
│   ├── templates  html模板
│   ├── view_models  视图对应的json格式
│   └── web 蓝图和相关的视图
├── fisher.py 运行app

```

config拆分成两部分
```
├── secure.py #存放机密配置，如数据库信息等
├── setting.py #存放一般配置
```

### 鱼书涉及知识点？
1.如何设置通用的访问地址？

#### 设置通用的访问地址
```
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10)
```



## 蓝图
>1. 什么是蓝图？
>2. 如何使用蓝图？

### 什么是蓝图？

[什么是蓝图](https://spacewander.github.io/explore-flask-zh/7-blueprints.html)

<img src="/images/blueprint.png" width="500" hegiht="313" align=center />


对于一个博客应用来说，经常会区分用户使用站点和后台。
两者同属于一个应用，如果把两者分成两个应用，总有一些代码可以复用，例如数据库配置等。
但是，两者放在一起，耦合度又过高，不便于管理。

Flask的蓝图的作用就是，让每个蓝图相当于项目的子应用，独立存在。可以有自己的静态文件，静态目录，url规则。
每个蓝图互不影响，但又因为他们属于应用，可以共享应用配置。

所以对于大型应用，我们可以通过添加蓝图来扩展应用功能，而不至于影响原来的功能。

**注意**

Flask蓝图的注册时静态的，不支持可拔插。即应用运行后，便可以访问所有注册的蓝图。

### 如何使用蓝图？
1. 创建蓝图，命名web
2. 创建蓝图下的视图函数
3. 在应用中注册蓝图


[如何使用蓝图](http://www.bjhee.com/flask-ad6.html)

在鱼书项目中我创建/web目录用来初始化蓝图，并存放与web相关的视图
```
app
....
   └── web
       ├── __init__.py
       └── book.py
```

1.初始化蓝图

web/__init__.py 初始化蓝图，命名为web
```
from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import book

```

2.创建视图，使用web命名url

web/book.py
```
from . import web


@web.route('/book/search')
def search():
    return 'Hello world!'
```

3.注册蓝图

在app/__init__.py中
```
    from app.web import web
    app.register_blueprint(web
```
结果如图

<img src="/images/test.png" width="300" hegiht="313" align=center />

## 数据模型

### 数据库配置

```
pipenv install flask-sqlalchemy
pipenv install mysqlclient
```
在models文件夹中创建数据库模型
models/base.py
```
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

<img src="/images/book_data.png" width="400" hegiht="313" align=center />


models/book.py
```
from sqlalchemy import Column, Integer, String
from app.models.base import db


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未知')
    # 精装还是平装
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

```


然后在app/__init__.py中初始化数据库
```
from  app.models.base import db

#配置文件
app.config.from_object('app.secure')
app.config.from_object('app.setting')

#数据库初始化
   db.init_app(app)
   with app.app_context():
       db.create_all()

```

还要记住在配置中配置数据库信息

security.py
```
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

```

## API数据请求

#### 通过关键字查询

http://t.yushu.im/v2/book/search?q=红楼梦

<img src="/images/key_search.png" width="400" hegiht="313" align=center />

<img src="/images/key_search_2.png" width="400" hegiht="313" align=center />

```java
"books":[
        {
            "author":[
                "[清] 曹雪芹 著",
                "高鹗 续"
            ],
            "binding":"平装",
            "category":"小说",
            "id":1057,
            "image":"https://img1.doubanio.com/lpic/s1070959.jpg",
            "images":{
                "large":"https://img1.doubanio.com/lpic/s1070959.jpg"
            },
            "isbn":"9787020002207",
            "pages":"1606",
            "price":"59.70元",
            "pubdate":"1996-12",
            "publisher":"人民文学出版社",
            "subtitle":"",
            "summary":"《红楼梦》是一部百科全书式的长篇小说。以宝黛爱情悲剧为主线，以四大家族的荣辱兴衰为背景，描绘出18世纪中国封建社会的方方面面，以及封建专制下新兴资本主义民主思想的萌动。结构宏大、情节委婉、细节精致，人物形象栩栩如生，声口毕现，堪称中国古代小说中的经 典。\n由红楼梦研究所校注、人民文学出版社出版的《红楼梦》以庚辰（1760）本《脂砚斋重评石头记》为底本，以甲戌（1754）本、已卯（1759）本、蒙古王府本、戚蓼生序本、舒元炜序本、郑振铎藏本、红楼梦稿本、列宁格勒藏本（俄藏本）、程甲本、程乙本等众多版本为参校本，是一个博采众长、非常适合大众阅读的本子；同时，对底本的重要修改，皆出校记，读者可因以了解《红楼梦》的不同版本状况。\n红学所的校注本已印行二十五年，其间1994年曾做过一次修订，又十几年过去，2008年推出修订第三版，体现了新的校注成果和科研成果。\n关于《红楼梦》的作者，原本就有多种说法及推想，“前八十回曹雪芹著、后四十回高鹗续”的说法只是其中之一，这次修订中校注者改为“前八十回曹雪芹著；后四十回无名氏续，程伟元、高鹗整理”，应当是一种更科学的表述，体现了校注者对这一问题的新的认识。\n现在这个修订后的《红楼梦》是更加完善。",
            "title":"红楼梦",
            "translator":[

            ]
        },
```
#### 通过isbn查询
http://t.yushu.im/v2/book/isbn/9787501524044

```
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

```

#### 创建对应的类接收数据

spider/yushu_book.py
```

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

```

其中Http为获取数据的类,libs/helper.py

```
import requests


class HTTP:

    @classmethod
    def get(cls, url, return_json=True):
        r = requests.get(url)

        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

```

## 返回数据格式
我们需要返回给前端的数据和我们存储的数据格式是不同的，
所以我们需要给数据做特定地封装，以返回指定的格式。

view_models/book.py
```
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
        self.author = '、'.index(book['author'])
        self.summary = book['summary']
        self.image = book['image']
        self.isbn = book['isbn']
        self.price = book['price']
```

集合类型的返回格式

```

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

```

## 请求数据

### 添加form表单验证

```
pipenv install flask-wtf

```
```
from wtforms import StringField, Form, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


# DataRequired防止传入空字符串
class SearchForm(Form):
    """
    控制请求的关键字，如果q为空在则会返回长度不满足要求
    page给定默认值
    """

    q = StringField(validators=[DataRequired(), Length(min=1, max=30, message="长度不满足要求")])
    page = IntegerField(default=1, validators=[NumberRange(min=1, max=99)])

```

请求方式为
```
from . import web
from app.forms.book import SearchForm
from flask import request, flash, jsonify

from app.view_models.book import BookViewModel, BookCollection
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

    else:
        return form.errors

    return "hello"
```

1. 当请求地址为 http://0.0.0.0:5000/book/search?

```
{
q: [
"This field is required."
]
}
```
2. 当请求地址为 http://0.0.0.0:5000/book/search?q

```
{
q: [
"This field is required."
]
}

```

3. 当请求地址为 http://0.0.0.0:5000/book/search?q=9787501524044

```

hello
```

4. 当请求的地址长度大于100

```
{
q: [
"长度不满足要求"
]
}
```

### 请求代码

1. 验证请求信息是否合法
2. 判断是否为isbn
3. 获取请求数据，并封装成需要显示的格式

```
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

```

请求结果显示 http://0.0.0.0:5000/book/search?q=9787501524044
```
{
books: [
{
author: "蔡智恒",
image: "https://img3.doubanio.com/lpic/s1327750.jpg",
isbn: "9787501524044",
pages: "224",
price: "12.80",
publisher: "知识出版社",
summary: "你还没有试过，到大学路的麦当劳，点一杯大可乐，与两份薯条的约会方法吗？那你一定要读目前最抢手的这部网络小说——《第一次的亲密接触》。\n由于这部小说在网络上一再被转载，使得痞子蔡的知名度像一股热浪在网络上延烧开来，达到无国界之境。作者的电子信箱，每天都收到热情的网友如雪片飞来的信件，痞子蔡与轻舞飞扬已成为网络史上最发烧的网络情人。",
title: "第一次的亲密接触"
}
],
keyword: "9787501524044",
total: 1
}
```

请求结果显示 http://0.0.0.0:5000/book/search?q=红楼梦

```
books: [
{
author: "萨孟武",
image: "https://img1.doubanio.com/lpic/s1418087.jpg",
isbn: "9787563352890",
pages: "171",
price: "16.00元",
publisher: "广西师范大学出版社",
summary: "“满纸荒唐言，一把辛酸泪。都云作者痴，谁解其中味”。萨孟武先生以研究社会文化的角度来解读《红楼梦》，引领读者深入贾府的家庭生活，重新认识中国传统家庭，剖示传统社会的文化与伦理格局，演绎社会风气的流转，见解精微，启人心智，是一部别开生面、言近旨远的大家小书。",
title: "红楼梦与中国旧家庭"
},
{
author: "曹雪芹",
image: "https://img3.doubanio.com/lpic/s4466175.jpg",
isbn: "9787508823737",
pages: "1194",
price: "120.00元",
publisher: "龙门书局",
summary: "《蔡义江新评红楼梦(套装上下册)》由以下几个部分构成：第一，精心校勘的红楼梦原文，正本清源，摒弃各本常见谬误，严谨权威，在学界内此版本被誉为“蔡本”；第二，每回前均有题解，细论回目原貌，探讨回目精义；第三，每回后配有总评，从整体上赏鉴本回内容；第四，作者侧批与红楼梦正文分双栏排版，一一对应，解读精细，抽丝剥茧搬地为读者展现出红楼的艺术价值，评注中还收录了上千条脂批，以飨读者。第五，附编有多篇专题文章，系统化地阐述有关红楼的学术问题，是作者一生的心血凝集；另外《蔡义江新评红楼梦(套装上下册)》还附录了红楼的珍贵资料图片以及红楼梦人物关系图表，堪称红楼梦收藏的最佳版本。\n封面：",
title: "蔡义江新评红楼梦"
}
],
keyword: "红楼梦",
total: 34
}
```
