from flask import Flask, request,jsonify,send_from_directory,make_response,send_file
from extend import function,verify
import os,sys,json

操作 = function()
认证 = verify()
app = Flask(__name__)

@app.route('/')
def distribute():
        行为 = request.args.get('do')

        if 行为 == 'login':
            用户名 = request.args.get('username')
            密码 = request.args.get('password')
            if 操作.登录(用户名,密码):
                return jsonify({"msg":"Login"})
            else :
                return jsonify({"msg":"UserError"})

        elif 行为 == 'register':
            用户名 = request.args.get('username')
            密码 = request.args.get('password')
            邀请码 = request.args.get('invite')
            状态 = 操作.注册(用户名,密码,邀请码)
            if 状态 == 1:
                return jsonify({'msg':'Reg'})
            elif 状态 == 'nameerror':
                return jsonify({'msg':'UserError'})
            else :
                return jsonify({'msg':'RegError'})

        elif 行为 == 'check':
            用户名 = request.args.get('username')
            参数 = 操作.初始化(用户名)
            return jsonify({'username':参数[0], 'area':参数[1], 'seat':参数[2], 'invite':参数[3], 'date':参数[4], 'phone':参数[5], 'qq':参数[6]})

        elif 行为 == 'book':
            用户名 = request.args.get('username')
            座位 = request.args.get('seat')
            书库 = request.args.get('area')
            日期 = request.args.get('date')
            if 操作.预定(座位,日期,书库,用户名):
                return jsonify({'msg':'Booking'})
            else :
                return jsonify({'msg':'Booked'})

        elif 行为 == 'unbook':
            用户名 = request.args.get('username')
            if 操作.退订(用户名):
                return jsonify({'msg':'UnBook'})
            else :
                return jsonify({'msg':'error'})

        elif 行为 == 'phone':
            用户名 = request.args.get('username')
            手机 = request.args.get('phoneid')
            if 操作.手机(用户名,手机):
                return jsonify({'msg':'Phone'})

        elif 行为 == 'qq':
            用户名 = request.args.get('username')
            QQ = request.args.get('QQ')
            if 操作.QQ(用户名,QQ):
                return jsonify({'msg':'QQ'})

        elif 行为 == 'now':
            用户名 = request.args.get('username')
            书库 = request.args.get('area')
            书库,座位 = 操作.抢座(用户名,书库)
            if 书库 != 0:
                return jsonify({'area':书库,'seat':座位})
            else:
                return jsonify({'msg':'Error'})

        elif 行为 == 'getimg':
            Cookie,文件名 = 认证.验证码()
            return jsonify({"Cookie":Cookie,"img":文件名})

        elif 行为 == 'verify':
            Cookie = json.loads(request.args.get('cookie'))
            用户名 = request.args.get('username')
            密码 = request.args.get('password')
            验证码 = request.args.get('code')
            if 认证.登录(Cookie,用户名,密码,验证码) :
                return 'true'
            else :
                return 'false'

        else :
            return 'Powered By Flask Version0.1'

@app.route('/img/<img>')
def img(img):
    目录 = '/www/wwwroot/API/Library/img'
    响应 = make_response(
        send_from_directory(目录,img)
    )
    os.remove(目录+img)
    return 响应