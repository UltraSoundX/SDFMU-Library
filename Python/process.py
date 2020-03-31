from flask import Flask, request
from extend import function
操作 = function()
app = Flask(__name__)
@app.route('/')
def 路由():
        行为 = request.args.get('do')
        if 行为 == 'login':
            用户名 = request.args.get('username')
            密码 = request.args.get('password')
            return 操作.登录(用户名,密码)
        elif 行为 == 'register':
            return 操作.注册()
        elif 行为 == 'check':
            return 操作.初始化()
        elif 行为 == 'book':
            return 操作.预定()
        elif 行为 == 'unbook':
            return 操作.退订()
        elif 行为 == 'phone':
            return 操作.手机()
        elif 行为 == 'now':
            return 操作.抢座()
        elif 行为 == 'qq':
            return 操作.QQ()
        else :
            return 'Fuck U'
