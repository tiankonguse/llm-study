from flask import Flask,request,make_response,render_template,session

app = Flask(__name__)
# 路由 (Routing)
@app.route('/')
def home():
    return 'Welcome to the Home Page!'

# 路由 (Routing)
@app.route('/about')
def about():
    return 'This is the About Page.'

# 视图函数 (View Functions)
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

# 请求对象 (Request Object)
@app.route('/submit', methods=['GET'])
def submit():
    username = request.form.get('username')
    return f'Hello, {username}!'
# 响应对象 (Response Object)
@app.route('/custom_response')
def custom_response():
    response = make_response('This is a custom response!')
    response.headers['X-Custom-Header'] = 'Value'
    return response


# 模板 (Templates)
@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

# 会话 (Sessions)
# 自动生成的密钥
app.secret_key = 'your_secret_key_here'
@app.route('/set_session/<username>')
def set_session(username):
    session['username'] = username
    return f'Session set for {username}'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    return f'Hello, {username}!' if username else 'No session data'


# 错误处理 (Error Handling)
@app.errorhandler(404)
def page_not_found(e):
    return 'Page not found', 404

@app.errorhandler(500)
def internal_server_error(e):
    return 'Internal server error', 500


# 检查这个模块是否被直接运行，而不是被其他模块导入。如果是直接运行，下面的代码块将被执行。
# 主程序入口
if __name__ == '__main__':
    # 运行Flask应用，开启调试模式
    # debug=True 参数会启动调试模式，这意味着应用会在代码改变时自动重新加载，并且在发生错误时提供一个调试器。
    app.run(debug=True)