import pymysql,string,random,time,hashlib,requests,datetime,json
from io import BytesIO
from requests.cookies import RequestsCookieJar
from urllib.parse import quote

try:
    数据库 = pymysql.connect("localhost","Radiology-Library","Radiology-Library","Library")
    数据库.autocommit(1)
    print('\033[32mAPI:Ready')
    print('\033[0m')
except:
    print('\033[31m数据库连接失败')
    print('\033[33mWeb API:Down')
    print('\033[32m验证接口：Ready')
    print('\033[0m')
    

class Verify:

    def sendmsg(self,QQ,msg):
        url = "http://lab.radiology.link:5700/send_private_msg?user_id="+str(QQ)+"&message="+str(msg)
        requests.get(url)
        return 0

    def 获取Cookie(self):
        url = "http://jwc.sdfmu.edu.cn/academic/common/security/login.jsp"
        Cookie = requests.utils.dict_from_cookiejar(requests.get(url).cookies)
        return Cookie
    
    def 验证码(self,QQ):
        Cookie = self.获取Cookie()
        游标 = 数据库.cursor()
        更新Cookie = 'UPDATE `user` SET `cookie`="%s" WHERE `qq`="%d"' % (str(Cookie),QQ)
        游标.execute(更新Cookie)
        url = 'http://jwc.sdfmu.edu.cn/academic/getCaptcha.do'
        验证码二进制 = requests.get(url,cookies=Cookie).content
        文件名 = "/www/wwwroot/api/Library/img/"+str(hashlib.md5(验证码二进制).hexdigest())+".jpg"
        with open(文件名, "wb") as f:
            f.write(验证码二进制)
            f.close()
        文件名 = str(hashlib.md5(验证码二进制).hexdigest())+".jpg"
        return 文件名
    
    def 登录(self,QQ,用户名,密码,验证码):
        游标 = 数据库.cursor()
        获取Cookie = "SELECT  `cookie` FROM `user` WHERE `qq`='%s'"%(QQ)
        游标.execute(获取Cookie)
        Cookie = 游标.fetchone()[0]
        Cookie = eval(Cookie)
        header = {"content-type":"application/x-www-form-urlencoded"}
        载荷 = "j_username="+str(用户名)+"&j_password="+quote(str(密码))+"&j_captcha="+str(验证码)
        url = "http://jwc.sdfmu.edu.cn/academic/j_acegi_security_check"
        请求 = requests.post(url,data=载荷,headers=header,cookies=Cookie)
        if 请求.url == 'http://jwc.sdfmu.edu.cn/academic/index_new.jsp':
            self.更改绑定(QQ,用户名)
            return 1
        else:
            return 0
    
    def 绑定(self,QQ,id):
        游标 = 数据库.cursor()
        绑定学号 = "UPDATE `user` SET `qq`='%s' WHERE `studentid`='%s'" % (QQ,id)
        if 游标.execute(绑定学号) == 1 :
            return 1
        else :
            return 0
    
    def 更改绑定(self,QQ,id):
        游标 = 数据库.cursor()
        绑定学号 = "UPDATE `user` SET `studentid`='%s' WHERE `qq`='%s'" % (id,QQ)
        if 游标.execute(绑定学号):
            self.sendmsg(QQ,'学号成功更改 回复 绑定 查询当前学号')
            return 0
        else :
            self.sendmsg(QQ,'学号成功更改 回复 绑定 查询当前学号')

class Appoint :

    def check(self,QQ):
        游标 = 数据库.cursor()
        查询 = "SELECT `studentid` FROM `user` WHERE `qq` = '%s'" % (QQ)
        if 游标.execute(查询) == 1:
            参数 = 游标.fetchone()
            return 参数[0]
        else:
            return 0

    def sendmsg(self,QQ,msg):
        url = "http://lab.radiology.link:5700/send_private_msg?user_id="+str(QQ)+"&message="+str(msg)
        requests.get(url)
        return 0

    def cancel(self,QQ):
        游标 = 数据库.cursor()
        清除 = "UPDATE `user` SET `seat`=NULL,`datepicker`=NULL,`area`=NULL WHERE `qq`='%d'"%(QQ)
        if 游标.execute(清除) == 1:
            self.sendmsg(QQ,'预约取消成功!')
        else:
            self.sendmsg(QQ,'暂无可使用的预约')
            
    def appointnow(self,QQ):
        游标 = 数据库.cursor()
        查询 = "SELECT `studentid` FROM `user` WHERE `qq` = '%s'" % (QQ)
        总书库 = (4,5,8,9,10,11,14,15)
        if 游标.execute(查询) == 1:
            id = 游标.fetchone()[0]
            area = 总书库[random.randint(0,7)]
            url = "https://api.radiology.link/Library/RestController.php/?do=now&username="+str(id)+"&area="+str(area)
            recv = requests.get(url).json()
            if 'msg' in recv :
                self.sendmsg(QQ,'预约失败，是否已有预约或者重试一次')
            if len(recv) == 2 :
                area = recv['area']
                seat = recv['seat']
                msg = '抢座成功，第'+str(area)+'书库，请在30分钟内到达图书馆签到'
                self.sendmsg(QQ,msg)
        else :
            self.sendmsg(QQ,'您是否绑定学号了？回复 绑定 查看绑定的学号')
    
    def appoint(self,QQ):
        游标 = 数据库.cursor()
        总书库 = (4,5,8,9,10,11,14,15)
        查询 = "SELECT `studentid` FROM `user` WHERE `qq` = '%s'" % (QQ)
        日期 = datetime.datetime.now()+datetime.timedelta(1)
        日期 = 日期.strftime('%Y-%m-%d')
        if 游标.execute(查询) == 1:
            参数 = 游标.fetchone()
            用户 = 参数[0]
            area = random.randint(0,7)
            书库 = 总书库[area]
            if 书库 == 4:
                seat = random.randint(1,56)
                位置 = 1333 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)

            if 书库 == 5:
                seat = random.randint(1,100)
                位置 = 1389 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)
            
            if 书库 == 8:
                seat = random.randint(1,56)
                位置 = 2325 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)
            
            if 书库 == 9:
                seat = random.randint(1,100)
                位置 = 1729 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)

            if 书库 == 10:
                seat = random.randint(1,56)
                位置 = 1829 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)
            
            if 书库 == 11:
                seat = random.randint(1,100)
                位置 = 1885 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)

            if 书库 == 14:
                seat = random.randint(1,56)
                位置 = 2169 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)

            if 书库 == 15:
                seat = random.randint(1,100)
                位置 = 2225 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)
            
            return 0