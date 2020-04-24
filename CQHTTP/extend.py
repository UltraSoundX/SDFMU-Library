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

def 邀请码生成(位数):
    total = string.digits +string.ascii_letters
    key = ''
    for i in range(1,位数+1):
        key += random.choice(total) #获取随机字符或数字
        if i % 4 == 0 and i !=位数: #每隔4个字符增加'-'
            key += '-'
    return key    

class Verify:

    def 邀请码(self,QQ):
        游标 = 数据库.cursor()
        查询邀请码 = "SELECT `invite` FROM `user` WHERE `qq`='%s'"%(QQ)
        if 游标.execute(查询邀请码):
            邀请码 = 游标.fetchone()[0]
            msg = "您的邀请码是"+str(邀请码)
            self.sendmsg(QQ,msg)
            return 0
        else :
            self.sendmsg(QQ,'请绑定或注册后查询')
            return 0

    def 校验(self,id,QQ):
        密码 = hashlib.md5()
        密码.update(str(id).encode("utf-8"))
        密码 = 密码.hexdigest()
        url = "http://202.194.232.138:85/api.php/login?from=mobile&password="+str(密码)+"&username=" +str(id)
        请求 = requests.get(url).json()
        if 请求['status'] == 0:
            self.sendmsg(QQ,'请联系 图书馆 进行预约系统的密码重置 \n重置为您的学号')
            return 0
        else :
            self.sendmsg(QQ,'恭喜您，无需修改图书馆登录密码')
            return 0

    def sendmsg(self,QQ,msg):
        url = "http://lab.radiology.link:5700/send_private_msg?user_id="+str(QQ)+"&message="+str(msg)
        requests.get(url)
        return 0

    def 获取Cookie(self):
        url = "http://jwc.sdfmu.edu.cn/academic/common/security/login.jsp"
        Cookie = requests.utils.dict_from_cookiejar(requests.get(url).cookies)
        return Cookie
    
    def 注册(self,学号,密码,验证码,邀请码,QQ):
        游标 = 数据库.cursor()
        查询邀请码 = "SELECT * FROM `invitecode` WHERE `invite` = '%s'" % (邀请码)
        if 游标.execute(查询邀请码) == 0:
            self.sendmsg(QQ,'找不到邀请码，可回复 人工 寻求帮助 或 找别人要邀请码')
            return 0
        获取Cookie = "SELECT `cookie` FROM `verify` WHERE `verify`='%s'" % (QQ)
        游标.execute(获取Cookie)
        Cookie = 游标.fetchone()[0]
        Cookie = eval(Cookie)
        header = {"content-type":"application/x-www-form-urlencoded"}
        载荷 = "j_username="+str(学号)+"&j_password="+quote(str(密码))+"&j_captcha="+str(验证码)
        url = "http://jwc.sdfmu.edu.cn/academic/j_acegi_security_check"
        请求 = requests.post(url,data=载荷,headers=header,cookies=Cookie)
        if 请求.url == 'http://jwc.sdfmu.edu.cn/academic/index_new.jsp':
            新邀请码 =  邀请码生成(5)
            注册 = "INSERT INTO `user`(`studentid`, `password`,`qq`,`invite`) VALUES ('%s','%s','%s','%s')" % (学号,学号,QQ,新邀请码)
            try:
                if 游标.execute(注册):
                    删除邀请码 = "DELETE FROM `invitecode` WHERE `invite` = '%s'" % (邀请码)
                    增加新邀请码 = "INSERT INTO `invitecode`(`invite`) VALUES ('%s')" % (新邀请码)
                    更改邀请状态 = "UPDATE `user` SET `invite`='%s' WHERE `invite`='%s'" % ('已邀请',邀请码)
                    if 邀请码 != 'fighting':
                        游标.execute(删除邀请码)
                    游标.execute(更改邀请状态)
                    游标.execute(增加新邀请码)
                    self.sendmsg(QQ,'注册成功\n网页端:https://lab.radiology.link\n默认登录密码为学号')
            except:
                self.sendmsg(QQ,'发生了错误，是不是注册过了')
        else:
            self.sendmsg(QQ,'发生了错误，请重新发送 注册 ')
            return 0

    def 注册验证码(self,QQ):
        Cookie = self.获取Cookie()
        游标 = 数据库.cursor()
        注册Cookie = 'INSERT INTO `verify`(`verify`, `cookie`) VALUES ("%s","%s")' % (QQ,str(Cookie))
        try:
            游标.execute(注册Cookie)
        except:
            更新Cookie = 'UPDATE `verify` SET `cookie`="%s" WHERE `verify`="%s"' % (Cookie,QQ)
            游标.execute(更新Cookie)
        url = 'http://jwc.sdfmu.edu.cn/academic/getCaptcha.do'
        验证码二进制 = requests.get(url,cookies=Cookie).content
        文件名 = "/www/wwwroot/api/Library/img/"+str(hashlib.md5(验证码二进制).hexdigest())+".jpg"
        with open(文件名, "wb") as f:
            f.write(验证码二进制)
            f.close()
        文件名 = str(hashlib.md5(验证码二进制).hexdigest())+".jpg"
        return 文件名

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
            print (url)
            print (recv)
            if 'msg' in recv :
                self.sendmsg(QQ,'预约失败\n是否已有预约或者重试一次')
            if len(recv) == 2 :
                area = recv['area']
                seat = recv['seat']
                msg = '抢座成功，第'+str(area)+'书库，请在30分钟内到达图书馆签到'
                self.sendmsg(QQ,msg)
        else :
            self.sendmsg(QQ,'您是否绑定学号了？\n回复 绑定 查看绑定的学号')
    
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
        else:
            self.sendmsg(QQ,'请前往\nhttps://lab.radiology.link/signup.html 进行注册 或 \n回复 注册（试运行）')
        return 0