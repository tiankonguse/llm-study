# Flask


https://dormousehole.readthedocs.io/en/latest/
https://www.runoob.com/flask/flask-tutorial.html

Flask 官网：https://flask.palletsprojects.com/
Flask 中文文档：https://flask.palletsprojects.com/zh-cn/stable/quickstart/
Flask 源码：https://github.com/pallets/flask/


Flask 是一个轻量级 WSGI（Web Server Gateway Interface） 网络应用框架
Flask 依赖 Werkzeug WSGI 套件、 Jinja 模板引擎和 Click CLI 套 件。

- Flask 应用实例：Flask 的核心是应用实例，通过创建 Flask 对象来初始化应用。
- 路由和视图函数：路由将 URL 映射到视图函数，视图函数处理请求并返回响应。
- 模板系统：Flask 使用 Jinja2 模板引擎来渲染 HTML 页面，将数据动态插入到页面中。
- 请求和响应：Flask 处理 HTTP 请求并生成响应，支持多种 HTTP 方法（如 GET、POST）。


## 环境搭建

Flask 需要 Python 3.6 及以上版本，先确保你已安装 Python 3。

```
conda activate llm-study
pip install flask
python 01.helloword.py
```


## 01. helloword


默认关闭 Debug 模式，端口为 5000.  


```bash
python 01.helloword.py
#  * Serving Flask app '01.helloword'
#  * Debug mode: on
#  * Running on http://127.0.0.1:5000
# Press CTRL+C to quit
#  * Restarting with stat
#  * Debugger is active!
#  * Debugger PIN: 134-743-044
# 127.0.0.1 - - [30/Mar/2025 16:20:47] "GET / HTTP/1.1" 200 -
```

## 基本概念

* 路由：路由是 URL 到 Python 函数的映射。Flask 允许你定义路由，这样当特定的 URL 被访问时，就会调用相应的函数。
* 视图函数：视图函数是处理请求并返回响应的 Python 函数。它们通常接收请求对象作为参数，并返回响应对象。
* 请求对象：请求对象包含了客户端发送的请求信息，如请求方法、URL、请求头、表单数据等。
* 响应对象：响应对象包含了发送给客户端的响应信息，如状态码、响应头、响应体等。
* 模板：Flask 使用 Jinja2 模板引擎来渲染 HTML 模板。模板允许你将 Python 代码嵌入到 HTML 中，从而动态生成网页。
* 应用工厂：应用工厂是一个 Python 函数，它创建并返回一个 Flask 应用实例。这允许你配置和初始化你的应用，并且可以创建多个应用实例。
* 配置对象：Flask 应用有一个配置对象，你可以使用它来设置各种配置选项，如数据库连接字符串、调试模式等。
* 蓝图：蓝图是 Flask 中的一个组织代码的方式，它允许你将相关的视图函数、模板和静态文件组织在一起，并且可以在多个应用中重用。
* 静态文件：静态文件是不会被服务器端执行的文件，如 CSS、JavaScript 和图片文件。Flask 提供了一个简单的方法来服务这些文件。
* 扩展：Flask 有许多扩展，可以添加额外的功能，如数据库集成、表单验证、用户认证等。
* 会话：Flask 使用客户端会话来存储用户信息，这允许你在用户浏览你的应用时记住他们的状态。
* 错误处理：Flask 允许你定义错误处理函数，当特定的错误发生时，这些函数会被调用。


### 1. 路由 (Routing)

路由是 URL 到 Python 函数的映射。


### 2. 视图函数 (View Functions)

视图函数是处理请求并返回响应的 Python 函数。它们通常接收请求对象作为参数，并返回响应对象，或者直接返回字符串、HTML 等内容。

