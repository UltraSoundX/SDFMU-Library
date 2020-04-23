from flask import Flask, request,jsonify,send_from_directory,make_response,send_file
import os,sys,json,requests
from extend import Appoint
import _thread
import time

预约 = Appoint()
app = Flask(__name__)

def sendmsg(userid):
    time.sleep(5)
    id = 预约.check(userid)
    print(id)
    if id != 0:
        msg = "欢迎使用山一医图书馆预约\nQQ已经绑定账号："+str(id) + "\n快速预约请发送：预约\n取消预约请发送：取消预约"
        url = "http://127.0.0.1:5700/send_private_msg?user_id="+str(userid)+"&message="+str(msg)
        requests.get(url)
        return 0
    else :
        msg = "欢迎使用山一医图书馆预约\n请前往 https://lab.radiology.link/signup.html 进行注册\n 注册后打开 https://lab.radiology.link/ 绑定QQ开始快速预约"
        url = "http://127.0.0.1:5700/send_private_msg?user_id="+str(userid)+"&message="+str(msg)
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
        print (recv['raw_message'])
        if msg == '预约':
            预约.appoint(userid)
            return 'Success'
        if msg == '取消预约':
            预约.cancel(userid)
            return 'Success'
        reply = {
            'reply':"指定位置预约请前往 https://lab.radiology.link/ \n发送 预约 至机器人可快速预约\n发送 取消预约 可快速取消"
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