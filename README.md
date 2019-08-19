# fisher
鱼书笔记

### 依赖管理工具pipenv
>1. 什么是pipenv?
>2. 为什么要使用pipenv？
>3. 如何使用pipenv？

#### 什么是pipenv？
pipenv是Kenneth Reitz在2017年1月发布的Python依赖管理工具，可以看做是pip和virtualenv的组合体，他基于Pipfile的依赖记录方式，而不是requirements.txt的记录方式。

#### 为什么使用pipenv？
pipenv会自动帮你管理虚拟环境和依赖文件，并提供了一系列命令和选项来帮助你实现各种依赖和环境管理相关的操作。总之，它更方便，完善，安全。

#### 如何使用pipenv？

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


#### pipenv安装速度慢怎么解决？
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
#### 使用pycharm
我们使用pycharm打开项目，根据提示安装pipenv，就完成了环境部署。
查看terminal，结果如下
```
(fisher) Mac-mini:fisher h$
```

### 鱼书项目简介
>1. 鱼书有什么功能？
>2. 涉及哪些方面的知识

#### 鱼书有什么功能？

<img src="/images/fisher.png" width="500" hegiht="313" align=center />

### 蓝图
>1. 什么是蓝图？
>2. 如何使用蓝图？

#### 什么是蓝图？
<img src="/images/blueprint.png" width="500" hegiht="313" align=center />


对于一个博客应用来说，经常会区分用户使用站点和后台。
两者同属于一个应用，如果把两者分成两个应用，总有一些代码可以复用，例如数据库配置等。
但是，两者放在一起，耦合度又过高，不便于管理。

Flask的蓝图的作用就是，让每个蓝图相当于项目的子应用，独立存在。可以有自己的静态文件，静态目录，url规则。
每个蓝图互不影响，但又因为他们属于应用，可以共享应用配置。

所以对于大型应用，我们可以通过添加蓝图来扩展应用功能，而不至于影响原来的功能。

**注意**

Flask蓝图的注册时静态的，不支持可拔插。即应用运行后，便可以访问所有注册的蓝图。

#### 如何使用蓝图？
