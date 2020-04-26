from flask import Flask, request, jsonify, send_from_directory, make_response, send_file
import os, sys, json, requests
from extend import Appoint, Verify
import _thread, threading
import time, re
from urllib.parse import quote

预约 = Appoint()
认证 = Verify()
app = Flask(__name__)


def sendmsg(userid):
    time.sleep(3)
    id = 预约.check(userid)
    print(id)
    if id != 0:
        msg = "欢迎使用山一医图书馆预约\nQQ已经绑定学号：" + str(
            id
        ) + "\n快速预约请发送：预约\n取消预约请发送：取消预约\n绑定QQ请发送：绑定 你的学号\n绑定学号请发送：认证\n其他指令请发送：帮助"
        url = "http://lab.radiology.link:5700/send_private_msg?user_id=" + str(
            userid) + "&message=" + str(msg)
        requests.get(url)
        msg = "请注意！如果在微信图书馆公众号的预约系统中更改过登录密码，请返回 图书馆公众号 修改密码为你的学号\n否则预约失败\n检验是否需要修改请回复 登录 你的学号\n其他指令请发送：帮助"
        url = "http://lab.radiology.link:5700/send_private_msg?user_id=" + str(
            userid) + "&message=" + str(msg)
        requests.get(url)
        return 0
    else:
        msg = "欢迎使用山一医图书馆预约\n如果已经注册网页版账号请回复 绑定 学号 进行账号绑定\n如没有请前往 https://lab.radiology.link/signup.html 进行注册\n注册后打开 https://lab.radiology.link/ 绑定QQ开始快速预约 \n或者回复 注册 进行账号注册（实验功能）"
        url = "http://lab.radiology.link:5700/send_private_msg?user_id=" + str(
            userid) + "&message=" + str(msg)
        requests.get(url)
        msg = "请注意！如果在微信图书馆公众号的预约系统中更改过登录密码，请返回 图书馆公众号 修改密码为你的学号\n否则预约失败\n检验是否需要修改请回复 登录 你的学号\n其他指令请发送：帮助"
        url = "http://lab.radiology.link:5700/send_private_msg?user_id=" + str(
            userid) + "&message=" + str(msg)
        requests.get(url)
        return 0


@app.route('/', methods=['POST'])
def receive():
    recv = json.loads(request.data.decode('utf-8'))
    msgtype = recv['post_type']
    userid = recv['user_id']

    if msgtype == 'request':
        userid = recv['user_id']
        reply = {'approve': True}
        threading.Thread(target=sendmsg, args=(userid, )).start()
        #_thread.start_new_thread(sendmsg,(userid,))
        return jsonify(reply)

    if msgtype == 'message':
        msg = recv['message']
        raw = recv['raw_message']
        msgfrom = recv['message_type']
        print(msgfrom)
        print(msg)
        if msgfrom == "private":
            try:
                print(raw)
                if '人工' in msg:
                    url = "http://api.radiology.link:5700/send_private_msg"
                    message = "有问题请联系：[CQ:contact,id=951671556,type=qq]"
                    payload = {"user_id": userid, "message": message}
                    requests.post(url, data=payload)
                    return 'Success'

                if '邀请码' in msg:
                    认证.sendmsg(userid, '获取您的邀请码需已经绑定QQ')
                    认证.邀请码(userid)
                    return 'Success'

                if '注册' in msg:
                    if ',' in msg or '，' in msg:
                        msg = msg.replace(" ", "")
                        msg = msg.replace("，", ",")[2:]
                        msg = re.split(',', msg)
                        学号 = msg[0]
                        密码 = msg[1]
                        验证码 = msg[2]
                        邀请码 = msg[3]
                        认证.注册(学号, 密码, 验证码, 邀请码, userid)
                        return ('Success')
                    else:
                        认证.sendmsg(userid,
                                   "正在从 教育在线 获取验证码...\n该功能仅为试验功能 开放时间不定")
                        url = "http://api.radiology.link:5700/send_private_msg"
                        jpg = "https://api.radiology.link/Library/img/" + str(
                            认证.注册验证码(userid))
                        message = "验证码：[CQ:image,file=" + str(
                            jpg
                        ) + "]\n请回复\n注册 教育在线学号,教育在线密码,验证码,邀请码 用逗号分隔,看不清请重新回复注册\n需要邀请码请回复 人工 | 或者试试公用邀请码 fighting"
                        payload = {"user_id": userid, "message": message}
                        requests.post(url, data=payload)
                        return 'Success'
                if '登录' in msg or '登陆' in msg:
                    if " " in msg:
                        msg = msg.replace(" ", "")
                        id = msg[2:]
                        认证.校验(id, userid)
                        return "Success"
                    else:
                        reply = {'reply': "回复 登录 你的学号"}
                        return jsonify(reply)
                try:
                    if msg == '预约':
                        预约.appoint(userid)
                        return 'Success'
                    if msg == '取消预约':
                        预约.cancel(userid)
                        return 'Success'
                    if '认证' in msg:
                        if "," in msg or "，" in msg:
                            msg = msg.replace("，", ",")
                            raw = msg.replace(" ", "")[2:]
                            verify = re.split(",", raw)
                            id = verify[0]
                            password = verify[1]
                            code = verify[2]
                            if 认证.登录(userid, id, password, code):
                                reply = {'reply': "认证成功"}
                                return jsonify(reply)
                            else:
                                reply = {'reply': "认证失败，请重试"}
                                return jsonify(reply)
                        认证.sendmsg(userid, "正在获取验证码...")
                        url = "http://api.radiology.link:5700/send_private_msg"
                        jpg = "https://api.radiology.link/Library/img/" + str(
                            认证.验证码(userid))
                        message = "验证码：[CQ:image,file=" + str(
                            jpg
                        ) + "]\n请回复\n认证 教育在线学号,教育在线密码,验证码\n用逗号分隔,看不清请重新回复认证"
                        payload = {"user_id": userid, "message": message}
                        requests.post(url, data=payload)
                        return 'Success'
                    if '抢座' in msg:
                        if '确认' in msg:
                            预约.appointnow(userid)
                            return 'Success'
                        reply = {'reply': "抢座执行后无法取消\n确定执行请回复\n抢座 确认"}
                        return jsonify(reply)
                    if '绑定' in msg:
                        msg = msg.replace(" ", "")
                        id = msg[2:]
                        if id == "":
                            id = 预约.check(userid)
                            reply = {'reply': "请输入 绑定 你的学号\n现在已经绑定的学号是" + id}
                            return jsonify(reply)
                        try:
                            if 认证.绑定(userid, id):
                                reply = {'reply': "学号绑定成功"}
                                return jsonify(reply)
                            else:
                                reply = {'reply': "学号绑定失败"}
                                return jsonify(reply)
                        except:
                            reply = {
                                'reply':
                                "请检查是否注册\n请前往 https://lab.radiology.link/signup.html 进行注册"
                            }
                            return jsonify(reply)
                except:
                    reply = {
                        'reply':
                        "请前往\nhttps://lab.radiology.link/signup.html 进行注册 或 \n回复 注册（试运行）"
                    }
                    return jsonify(reply)
                reply = {
                    'reply':
                    "指定位置预约请前往 https://lab.radiology.link/ \n发送 预约 至机器人可快速预约\n发送 取消预约 可快速取消\n发送 抢座 可实时抢座\n发送 绑定 可绑定QQ \n发送 认证 进行学号绑定更换\n发送 人工 即可寻求人工帮助\n发送 邀请码 获得新人邀请码\n以上功能均需注册 请前往\nhttps://lab.radiology.link/signup.html 进行注册 或者发送 注册 （实验功能)\n以上功能均需要校验您是否能正常登录图书馆\n请务必回复 登录 ！谢谢"
                }
                return jsonify(reply)
            except:
                reply = {"reply": "触发错误机制，已经向管理员发送错误，请发送 人工 寻求帮助"}
                return jsonify(reply)
            return "Private Success"

        if msgfrom == "group":
            if "夸" in raw:
                url = "https://chp.shadiao.app/api.php"
                msg = "\n" + requests.get(url).text
                reply = {"reply": msg}
                return jsonify(reply)
            if "杭州人" in raw:
                url = "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"
                msg = "[CQ:at,qq=872946892]\n" + requests.get(url).text
                reply = {"group_id": "618257920", "message": msg}
                group_url = "http://lab.radiology.link:5700/send_group_msg"
                requests.post(group_url, data=reply)
                return "Success"
            if "济南人" in raw:
                url = "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"
                msg = "[CQ:at,qq=951671556]\n" + requests.get(url).text
                reply = {"group_id": "618257920", "message": msg}
                group_url = "http://lab.radiology.link:5700/send_group_msg"
                requests.post(group_url, data=reply)
                return "Success"
            if "乳山人" in raw:
                url = "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"
                msg = "[CQ:at,qq=768621530]\n" + requests.get(url).text
                reply = {"group_id": "618257920", "message": msg}
                group_url = "http://lab.radiology.link:5700/send_group_msg"
                requests.post(group_url, data=reply)
                return "Success"
            if "景阳冈人" in raw:
                url = "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"
                msg = "[CQ:at,qq=2313746232]\n" + requests.get(url).text
                reply = {"group_id": "618257920", "message": msg}
                group_url = "http://lab.radiology.link:5700/send_group_msg"
                requests.post(group_url, data=reply)
                return "Success"
            if "313396469" in raw and "at" in raw:
                if "骂" in raw or "嘴臭" in raw or "对线" in raw or "闸总" in raw or "?" in raw or "？" in raw or "NMSL" in raw or "批" in raw or "five" in raw or "傻" in raw or "妈" in raw or "死" in raw or "sb" in raw or "爹" in raw or "爸" in raw or "你" in raw or "逼" in raw or "w" in raw:
                    print('火力全开')
                    url = "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"
                    msg = "\n你骂你🐎呢？\n" + requests.get(url).text
                    reply = {"reply": msg}
                    return jsonify(reply)
                reply = {"reply": "\n@我找骂呢，小逼崽子？\n有种艾特我发个 对线 试试"}
                return reply
            if "我要上" in raw or "我想上" in raw:
                gfw = "https://siiam.es/plugins/QuickWebProxy/miniProxy.php?" + "http://" + raw[
                    4:]
                print(gfw)
                gfw = quote(gfw)
                api = "3LP7brJJItEdHm6c5b@ddd"
                dwz = "http://api.ft12.com/api.php?url=" + gfw + "&apikey=" + api
                msg = "\n你要的网址如下\n" + requests.get(dwz).text
                reply = {"reply": msg}
                return jsonify(reply)
            return "Group Success"

        return "MSG SUCCESS"


@app.route('/', methods=['GET'])
def send():
    return "REPLY SERVICE ONLINE"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
