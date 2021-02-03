import requests
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import logging

wozaixiaoyuan_token = "93235013-73be-40c2-b2e7-2a0542d912bb" 
#这里把token_code的内容换为你自己的token，具体看https://violetwsh.com/2021/01/10/wozaixiaoyuan/#more

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
#logger.addHandler(handler)#输出成为文件形式，宝塔下部署时建议关闭，其他时候可以打开。
logger.addHandler(console)

mail_host = "smtp.163.com"# SMTP服务器
mail_user = "@163.com" # 用户名，也就是提供SMTP服务的邮箱
mail_pass = ""    # 授权密码，非登录密码 
sender = '@163.com'    # 发件人邮箱，应该于用户名相同
receivers = ['@outlook.com']  # 接收邮件
title = '我在校园自动打卡提醒'  # 邮件主题

def sendEmail(content):
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        logger.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger.info(e)
    
def HealthCheckIn(time):
    headers = {
        'content-length' : '296',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    Hpostdata = {
        'answers' : '["0","36.5"]',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '甘亭街道',
        'street' : '东街',
        'areacode' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/health/save.json'
    s = requests.session()
    r = s.post(url, data=Hpostdata,headers=headers)
    t = r.text
    #经过测试，t返回的字典里会有一个状态码，登陆成功为0，不成功为-10，对应的就是第8个字符。
    if t[8] == '0' :
        sendEmail("晨检、健康打卡打卡成功。\n"+time)
        logger.info("健康打卡成功\t"+t+"\t"+time)
    else:
        sendEmail("晨检、健康打卡打卡失败!\n可能是token失效，请尽快重新输入。\n"+time)
        logger.warning("token失效\t"+t+"\t"+time)
    
def MorningCheck(time):
    headers = {
        'content-length' : '306',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    Mpostdata = {
        'answers' : '["0"]',
        'seq' : '1',
        'temperature' : '36.5',
        'userid' : '',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '甘亭街道',
        'street' : '东街',
        'myArea' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=Mpostdata, headers=headers)
    t = r.text
    logger.info("晨检打卡\t"+t+"\t"+time)
      
def NoonInspection(time):
    headers = {
        'content-length' : '134',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    postdata = {
        'answers' : '["0","36.5"]',
        'seq' : '2',
        'temperature' : '36.6',
        'userid' : '',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '甘亭街道',
        'street' : '东街',
        'myArea' : '610118',
        'areacode' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=postdata, headers=headers)
    t = r.text
    if t[8] == '0' :
        sendEmail("午检打卡成功。\n"+time)
        logger.info("午检打卡成功\t"+t+"\t"+time)
    else:
        sendEmail("午检打卡打卡失败!\n可能是token失效，请尽快重新输入。\n"+time)
        logger.warning("打卡失败\t"+t+"\t"+time)
    
if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "06:30:10" or time_now == "06:30:11":#不知道是奇数还是偶数
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            HealthCheckIn(time_send)#健康打卡
            MorningCheck(time_now)#晨检
            
        if time_now == "11:20:10" or time_now == "11:20:11":
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            NoonInspection(time_send)#午检
            
        time.sleep(2) # 停两秒
