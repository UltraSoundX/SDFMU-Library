from flask import Flask, request,jsonify,send_from_directory,make_response,send_file
import os,sys,json,requests
from extend import Appoint,Verify
import _thread
import time,re

预约 = Appoint()
认证 = Verify()
app = Flask(__name__)

def sendmsg(userid):
    time.sleep(5)
    id = 预约.check(userid)
    print(id)
    if id != 0:
        msg = "欢迎使用山一医图书馆预约\nQQ已经绑定学号："+str(id) + "\n快速预约请发送：预约\n取消预约请发送：取消预约\n绑定QQ请发送：绑定 你的学号\n重新绑定学号请发送：认证"
        url = "http://lab.radiology.link:5700/send_private_msg?user_id="+str(userid)+"&message="+str(msg)
        requests.get(url)
        return 0
    else :
        msg = "欢迎使用山一医图书馆预约\n如果已经注册网页版账号请回复 绑定 学号 进行账号绑定\n请前往 https://lab.radiology.link/signup.html 进行注册\n 注册后打开 https://lab.radiology.link/ 绑定QQ开始快速预约"
        url = "http://lab.radiology.link:5700/send_private_msg?user_id="+str(userid)+"&message="+str(msg)
        requests.get(url)
        return 0



@app.route('/', methods=['POST'])
def receive():
    recv = json.loads(request.data.decode('utf-8'))
    msgtype = recv['post_type']
    userid = recv['user_id']
    print (msgtype)
    if msgtype == 'message': 
        msg = recv['message']
        if msg == '预约':
            预约.appoint(userid)
            return 'Success'
        if msg == '取消预约':
            预约.cancel(userid)
            return 'Success'
        if '认证' in msg:
            if "," in msg or "，" in msg:
                msg = msg.replace("，",",")
                raw = msg.replace(" ","")[2:]
                verify = re.split(",",raw)
                id = verify[0]
                password = verify[1]
                code = verify[2]
                if 认证.登录(userid,id,password,code):
                    reply = {
                        'reply':"认证成功"
                    }
                    return jsonify(reply)
                else:
                    reply = {
                        'reply':"认证失败，请重试"
                    }
                    return jsonify(reply)
            认证.sendmsg(userid,"正在获取验证码...")
            url = "http://api.radiology.link:5700/send_private_msg"
            jpg = "https://api.radiology.link/Library/img/"+str(认证.验证码(userid))
            message = "验证码：[CQ:image,file=" + str(jpg) +"]\n请回复 认证 教育在线学号,教育在线密码,验证码 用逗号分隔,看不清请重新回复认证"
            payload = {"user_id":"951671556","message":message}
            a = requests.post(url,data=payload)
            return 'Success'
        if '抢座' in msg:
            reply = {
                    'reply':"抢座执行后无法取消 确定执行请回复\n抢座 确认"
                }
            return jsonify(reply)
            if '确认' in msg:
                预约.appointnow(userid)
                return 'Success'
        if '绑定' in msg:
            msg = msg.replace(" ","")
            id = msg[2:]
            if id == "":
                id = 预约.check(userid)
                reply = {
                    'reply':"请输入 绑定 你的学号\n现在已经绑定的学号是"+id
                }
                return jsonify(reply)
            try:
                if 认证.绑定(userid,id) :
                    reply = {
                        'reply':"学号绑定成功"
                    }
                    return jsonify(reply)
                else :
                    reply = {
                        'reply':"学号绑定失败"
                    }
                    return jsonify(reply)
            except:
                reply = {
                    'reply':"请检查是否注册\n请前往 https://lab.radiology.link/signup.html 进行注册"
                }
                return jsonify(reply)
        reply = {
            'reply':"指定位置预约请前往 https://lab.radiology.link/ \n发送 预约 至机器人可快速预约\n发送 取消预约 可快速取消\n发送 抢座 可实时抢座\n发送 绑定 可绑定QQ \n发送 认证 进行学号绑定更换"
        }
        return jsonify(reply)

    if msgtype == 'request':
        userid = recv['user_id']
        reply = {
            'approve':True
        }
        _thread.start_new_thread(sendmsg,(userid,))
        return jsonify(reply)        

@app.route('/',methods=['GET'])
def send():
    return "REPLY SERVICE ONLINE"

if __name__ == '__main__':
    app.run(
      host='0.0.0.0',
      port= 8080,
      debug=True
    )