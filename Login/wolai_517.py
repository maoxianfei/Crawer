#!/usr/bin/env python
# encoding: utf-8
import re
import base64
import requests
from bs4 import BeautifulSoup
import time
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
import smtplib
def decode(s1):
   return base64.b64decode(s1)

def getpoints():
    url='http://www.wolai66.com/sign_in'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Referer':'http://www.wolai66.com/sign_in'
    }

    s1='VENMMDA5MDI4OTU='
    s2='MjgwMzE2'
    wolaisession=requests.session()
    webData=wolaisession.get(url)
    # <meta content="JSnpUN9vbvGmGDFxmLbDQim6PP51jcO+Nzlkel51kps=" name="csrf-token" /></head><body class="businesses_custom_common_blue" data-current_user="false" style="margin: 0px;">
    # JSnpUN9vbvGmGDFxmLbDQim6PP51jcO+Nzlkel51kps=
    pattern_csrf_token=re.compile('<meta content="(.*?)" name="csrf-token" /></head><body class="businesses_custom_common_blue" data-current_user="false" style="margin: 0px;">')
    csrf_token=str(pattern_csrf_token.findall(webData.text))[2:-2]
    # print('str===>',csrf_token)
    postdata={
        'utf8':'✓',
        'authenticity_token':csrf_token,
        'from':'',
        'user_name':decode(s1),
        'user_password':decode(s2)
    }
    # 数据请返回302重定向，重新请求网址
    url1='http://www.wolai66.com/login'
    wolaisession.post(url1,data=postdata,headers=headers)
    url='http://www.wolai66.com/user'
    loginPage=wolaisession.get(url,headers=headers)
    # print(loginPage.text)
    pattern_money=re.compile('<em>(.*?)</em></span></div></div><div class="sidebar_list"')
    money=str(pattern_money.findall(loginPage.text))[2:-2]
    print('积分：',money)
    return money

def getinventory(url):
    webData = requests.get(url)
    soup = BeautifulSoup(webData.text, 'lxml')
    # 定位信息
    title = soup.select(
        '#commodity_top_wrap > div.commodity_info.clear > div.commodity_info_r > div > div.tb_title > h3')
    inventory = soup.select('#fesco_pro_inventory_quantity')
    prices=soup.select('#fesco_pro_price')
    price=str(prices)
    title1 = str(title)
    inventory1 = str(inventory)
    # print(price)
    # 使用正则筛选
    pattern = re.compile('>(.*)<')#商品名称
    title2 = pattern.findall(title1)
    price=pattern.findall(price)
    inventory2 = pattern.findall(inventory1)#商品库存
    title2=str(title2)[2:-2]
    inventory2=str(inventory2)[2:-2]
    price=str(price)[2:-2]   
    print('名称：%s元电子卡,实际价格%s元，数量：%s'%(title2,price,inventory2))
    if int(inventory2)>0:
        return True
def main():
    urls = {
        '300': 'http://www.wolai66.com/commodity?code=10172061270',
        '100': 'http://www.wolai66.com/commodity?code=10133563152',
        '200': 'http://www.wolai66.com/commodity?code=10152135133',
        '500': 'http://www.wolai66.com/commodity?code=10124884175',
        '107': 'http://www.wolai66.com/commodity?code=11066517741',#天狗107
        '1070': 'http://www.wolai66.com/commodity?code=10160124842',
        '214': 'http://www.wolai66.com/commodity?code=11063863053',#天狗214
        '321': 'http://www.wolai66.com/commodity?code=11065010573',#天狗321
        '150':'http://www.wolai66.com/commodity?code=10147528626',#京东E卡
        '208':'http://www.wolai66.com/commodity?code=10105122404',
        '201':'http://www.wolai66.com/commodity?code=10171476858',
    }
    info=[]
    global judge
    judge=0
    for url in urls:
        if getinventory(urls[url]):
            info.append(urls[url])
            judge=1
    return info

def email(url):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    msg = MIMEText(url, 'plain', 'utf-8')
    # 输入Email地址和口令:
    from_addr = 'tcltestmao@163.com'
    # from_addr = '1102836917@qq.com'
    password = '1234qwer'
    # password = 'bdxztldobaorgfag'
    # 输入收件人地址:
    # to_addr = '1102836917@kindle.cn'
    to_addr = '1102836917@qq.com'
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    msg['From'] = _format_addr('京东监视程序 <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('京东E卡到货了', 'utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server, 465) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__=='__main__':
    print("Created by xianfei.mao at Jan 23 2017")
    print("This demo to check E-card inventory")
    #检查剩余积分
    money=getpoints()
    #运行分钟数记录
    cnt=0
    while True:
        info=main()
        if judge==1:
            email(str(info))
            print("发现库存，发送邮件成功")
            print(str(info))
            time.sleep(14400)
        # input("Press any key  to END ")
        time.sleep(600)
        cnt+=1
        print("已经运行%d分钟"%(cnt*10))