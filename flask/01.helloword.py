# 导入Flask类
from flask import Flask

# __name__ 是一个特殊的 Python 变量，它在模块被直接运行时是 '__main__'，在被其他模块导入时是模块的名字。
# 创建Flask应用实例
app = Flask(__name__)

# 这是一个装饰器，用于告诉 Flask 哪个 URL 应该触发下面的函数。
# 定义路由，当访问根路径'/'时执行该视图函数
@app.route('/')
def hello_world():
    # 返回响应内容
    return 'Hello, World!'

# 检查这个模块是否被直接运行，而不是被其他模块导入。如果是直接运行，下面的代码块将被执行。
# 主程序入口
if __name__ == '__main__':
    # 运行Flask应用，开启调试模式
    # debug=True 参数会启动调试模式，这意味着应用会在代码改变时自动重新加载，并且在发生错误时提供一个调试器。
    app.run(debug=True)