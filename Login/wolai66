#!/usr/bin/env python
# encoding: utf-8
import re
import base64
import requests
from bs4 import BeautifulSoup

def decode(s1):
   return base64.b64decode(s1)

def getpoints():
    url='http://www.wolai66.com/sign_in'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Referer':'http://www.wolai66.com/sign_in'
    }
    s1=加密账号
    s2=加密密码
    wolaisession=requests.session()#更好的处理cookie
    webData=wolaisession.get(url)
    #从网站获取到csrf的值
    pattern_csrf_token=re.compile('<meta content="(.*?)" name="csrf-token" /></head><body class="businesses_custom_common_blue" data-current_user="false" style="margin: 0px;">')
    csrf_token=str(pattern_csrf_token.findall(webData.text))[2:-2]
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
    pattern_money=re.compile('<em>(.*?)</em></span></div></div><div class="sidebar_list"')
    money=str(pattern_money.findall(loginPage.text))[2:-2]
    print('积分：',money)

def getinventory(url):
    webData = requests.get(url)
    soup = BeautifulSoup(webData.text, 'lxml')
    # 定位信息
    title = soup.select('#commodity_top_wrap > div.commodity_info.clear > div.commodity_info_r > div > div.tb_title > h3')
    inventory = soup.select('#fesco_pro_inventory_quantity')
    prices=soup.select('#fesco_pro_price')
    #转字符串处理
    price=str(prices)
    title1 = str(title)
    inventory1 = str(inventory)
    #正则筛选过滤，构造pattern
    pattern = re.compile('>(.*)<')#商品名称
    title2 = pattern.findall(title1)
    price=pattern.findall(price)#商品价格
    inventory2 = pattern.findall(inventory1)#商品库存
    #字符串截取
    title2=str(title2)[2:-2]
    inventory2=str(inventory2)[2:-2]
    price=str(price)[2:-2]
    #格式化输出
    print('名称：%s元电子卡,实际价格%s元，数量：%s'%(title2,price,inventory2))

def main():
    urls = {
        '300': 'http://www.wolai66.com/commodity?code=10172061270',
        '100': 'http://www.wolai66.com/commodity?code=10133563152',
        '200': 'http://www.wolai66.com/commodity?code=10152135133',
        '500': 'http://www.wolai66.com/commodity?code=10124884175',
        '150': 'http://www.wolai66.com/commodity?code=10147528626',
    }
    for url in urls:
        getinventory(urls[url])

if __name__=='__main__':
    print("Created by xianfei.mao at Jan 23 2017")
    print("This demo to check E-card inventory")
    getpoints()
    main()
    input("Press any key  to END ")
