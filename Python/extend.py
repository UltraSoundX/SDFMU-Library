import pymysql,string,random,time,hashlib,requests
from io import BytesIO
from requests.cookies import RequestsCookieJar
from urllib.parse import quote

try:
    数据库 = pymysql.connect("localhost","Radiology-Library","Radiology-Library","Library")
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

class verify:

    def 获取Cookie(self):
        url = "http://jwc.sdfmu.edu.cn/academic/common/security/login.jsp"
        Cookie = requests.utils.dict_from_cookiejar(requests.get(url).cookies)
        return Cookie
    
    def 验证码(self):
        Cookie = self.获取Cookie()
        url = 'http://jwc.sdfmu.edu.cn/academic/getCaptcha.do'
        验证码二进制 = requests.get(url,cookies=Cookie).content
        文件名 = "/Users/haroldxin/Desktop/Code/temp/"+str(hashlib.md5(验证码二进制).hexdigest())+".jpg"
        with open(文件名, "wb") as f:
            f.write(验证码二进制)
            f.close()
        文件名 = str(hashlib.md5(验证码二进制).hexdigest())+".jpg"
        return Cookie,文件名
    
    def 登录(self,Cookie,用户名,密码,验证码):
        header = {"content-type":"application/x-www-form-urlencoded"}
        载荷 = "j_username="+str(用户名)+"&j_password="+quote(str(密码))+"&j_captcha="+str(验证码)
        url = "http://jwc.sdfmu.edu.cn/academic/j_acegi_security_check"
        请求 = requests.post(url,data=载荷,headers=header,cookies=Cookie)
        if 请求.url == 'http://jwc.sdfmu.edu.cn/academic/index_new.jsp':
            return 1
        else:
            return 0
    

class 抢座:
    日期 = time.strftime('%Y-%m-%d',time.localtime())

    def 获取预约信息(self,书库):
        url = "http://202.194.232.138:85/api.php/space_time_buckets/?area="+str(书库)+"&day="+str('2020-04-01')
        请求 = requests.get(url).json()
        if 请求['status'] :
            返回值 = []
            返回值.append(请求['data']['list'][0]['bookTimeId'])
            返回值.append(请求['data']['list'][0]['startTime'])
            return 返回值
        else :
            return 0
    
    def 获取Token(self,用户名):
        密码 = hashlib.md5()
        密码.update(str(用户名).encode("utf-8"))
        密码 = 密码.hexdigest()
        url = "http://202.194.232.138:85/api.php/login?from=mobile&password="+str(密码)+"&username=" +str(用户名)
        请求 = requests.get(url).json()
        return 请求['data']['_hash_']['access_token']
    
    def 订阅(self,用户名,书库,座位):
        Token = self.获取Token(用户名)
        预约代码 = self.获取预约信息(书库)[0]
        载荷 = {'access_token': Token, 'userid': 用户名, 'type': '1', 'id': 座位, 'segment': 预约代码}
        url = "http://202.194.232.138:85/api.php/spaces/"+str(座位)+"/book"
        请求 = requests.post(url, data=载荷).json()
        #print (请求)
        return 请求['status']

    def 抢座(self,用户名,书库):
        if self.获取预约信息(书库) == 0:
            return 0
        else:
            返回值 = self.获取预约信息(书库)
            预约代码 = 返回值[0]
            开始时间 = 返回值[1]
            url = "http://202.194.232.138:85/api.php/spaces_old/?area="+str(书库)+"&segment="+str(预约代码)+"&day="+str(self.日期)+"&startTime="+str(开始时间)+"&endTime=21:20" 
            请求 = requests.get(url).json()
            总位置 = 请求['data']['list']
            if isinstance(总位置,list):
                for 位置 in 总位置:
                    编号 = 位置['id']
                    状态 = 位置['status_name']
                    if 状态 == '空闲':
                        if self.订阅(用户名,书库,编号):
                            return 书库,编号
                        else:
                            return 0,0
            else:
                return 0,0

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

    def 抢座(self,用户名,书库):
        信标 = 抢座()
        return 信标.抢座(用户名,书库)