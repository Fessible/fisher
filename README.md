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
