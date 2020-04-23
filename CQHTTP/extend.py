import pymysql,string,random,time,hashlib,requests,datetime

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
        url = "http://127.0.0.1:5700/send_private_msg?user_id="+str(QQ)+"&message="+str(msg)
        requests.get(url)
        return 0

    def cancel(self,QQ):
        游标 = 数据库.cursor()
        清除 = "UPDATE `user` SET `seat`=NULL,`datepicker`=NULL,`area`=NULL WHERE `qq`='%d'"%(QQ)
        if 游标.execute(清除) == 1:
            self.sendmsg(QQ,'预约取消成功!')
        else:
            self.sendmsg(QQ,'暂无可使用的预约')
    
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
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n 取消预约请发送 取消预约'
                    self.sendmsg(QQ,msg)
                else:
                    msg = '预约失败，请重试一次预约指令或登录网页端进行预约 https://lab.radiology.link'
                    self.sendmsg(QQ,msg)

            if 书库 == 5:
                seat = random.randint(1,100)
                位置 = 1389 + seat - 1
                更新 = "UPDATE `user` SET `seat`='%s',`datepicker`='%s',`area`='%s' WHERE `studentid`='%s'" % (位置,日期,书库,用户)
                if 游标.execute(更新) == 1:
                    msg = '预约成功，第'+ str(area+1) + '书库，第' + str(seat) + '号 \n 取消预约请发送 取消预约'
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