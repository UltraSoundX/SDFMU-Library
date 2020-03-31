import pymysql
import string
import random
import requests

数据库 = pymysql.connect("localhost","Radiology-Library","Radiology-Library","Library")

def 邀请码生成(位数):
    total = string.digits +string.ascii_letters
    key = ''
    for i in range(1,位数+1):
        key += random.choice(total) #获取随机字符或数字
        if i % 4 == 0 and i !=位数: #每隔4个字符增加'-'
            key += '-'
    print(key)
    return key

class function:

    def 登录(self,用户名,密码):
        游标 = 数据库.cursor()
        查询 = "SELECT * FROM user WHERE studentid ='%s' AND password='%s'"%(用户名,密码)
        if 游标.execute(查询)== 1:
            return 1
        else :
            return 0

    def 注册(self,用户名,密码,邀请码):
        游标 = 数据库.cursor()
        查询邀请码 = "SELECT * FROM `invitecode` WHERE `invite`='%s'"%(邀请码)
        if 游标.execute(查询邀请码):
            新用户邀请码 = 邀请码生成(5)
            新建用户 = "INSERT INTO `user`(`studentid`, `password` , `invite`) VALUES ('%s','%s','%s')"%(用户名,密码,新用户邀请码)
            入库邀请码 = "INSERT INTO `invitecode`(`invite`) VALUES ('%s')" % (新用户邀请码)
            移除老邀请码 = "DELETE FROM `invitecode` WHERE `invite`='%s'"%(邀请码)
            更改邀请码状态 = "UPDATE `user` SET `invite`='已邀请' WHERE `invite`='%s'"%('已邀请')
            try:
                游标.execute(新建用户)
                游标.execute(新用户邀请码)
                游标.execute(移除老邀请码)
                游标.execute(更改邀请码状态)
                return 1
            except :
                return 'nameerror'
        else:
            return 'regerror'

    def 初始化(self,用户名):
        游标 = 数据库.cursor()
        初始化 = "SELECT studentid,area,seat,invite,phone,datepicker,qq FROM user WHERE studentid='%s'"%(用户名)
        游标.execute(初始化)
        参数 = 游标.fetchone()
        return 参数
        
    def 预定(self,位置,日期,书库,用户名):
        游标 = 数据库.cursor()
        检查 = "SELECT * FROM `user` WHERE `seat`=’%s' AND `datepicker`='%s'"%(位置,日期)
        if 游标.execute(检查):
            return 0
        else:
            定位 = "UPDATE `user` SET `seat`= '%s',`area`='%s',`datepicker`='%s' WHERE `studentid`= '%s'"%(位置,书库,日期,用户名)
            游标.execute(定位)
            return 1

    def 退订(self,用户名):
        游标 = 数据库.cursor()
        退订 = "UPDATE `user` SET `seat`= NULL,`area`=NULL,`datepicker`=NULL WHERE `studentid`= '%s'"%(用户名)
        游标.execute(退订)
        return 1

    def 手机(self,用户名,手机):
        游标 = 数据库.cursor()
        更新手机 = "UPDATE `user` SET `phone`='%s' WHERE `studentid`='%s'"%(手机,用户名)
        游标.execute(更新手机)
        return 1

    def QQ(self,用户名,QQ):
        游标 = 数据库.cursor()
        更新QQ = "UPDATE `user` SET `qq`='%s' WHERE `studentid`='%s'"%(QQ,用户名)
        游标.execute(更新QQ)
        return 1

    def 抢座(self,书库,用户名):
        url = 'https://api.radiology.link/Library/RestController.php/?do=now&username=%s&area=%s'%(用户名,书库)
        requests.get(url)
