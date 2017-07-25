# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
login_url=''
data_url=''

def login_user():
    headers={
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Referer': '',
            'Origin':'',
            "Upgrade-Insecure-Requests":"1",
            "Host":"",

    }
    postdata={
        "name":"user",
        "pass":"word",
    }
    # 实例化session
    wu_session=requests.session()
    # 访问网站获取cookie
    wu_session.get(login_url)
    # 提交数据
    wu_session.post(login_url,data=postdata,headers=headers)
    # 得到流量界面
    page=wu_session.get(data_url)
    a=re.compile('<td style="padding-left:50px">已用: (.*) 未用:(.*)</td>')
    result=a.findall(page.text)
    result_str="剩余流量：%s  已经使用：%s"%(result[0][1],result[0][0])
    print(result_str)



# 登陆方法一：cookie登陆
def login_cookie():
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': '',
        'Origin': '',
        "Upgrade-Insecure-Requests": "1",
        "Host": "kingss.win",
        "Cookie":"",
    }
    data=requests.get(data_url,headers=headers)
    soup=BeautifulSoup(data.text,'lxml')
    # 报错提示 nth-child 替换为 nth-of-type
    data_use=soup.select('#content > div > div.wrapper-md.control > div > section > div > div > div.row > div > div > div > table > thead > tr:nth-of-type(11) > td')#
    print(data_use)

def main():

    login_user()
    login_cookie()
