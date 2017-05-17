'''
这个爬虫主要知识点是对requests.session()的操作
v2exsession=requests.Session()
signin_data=v2exsession.get(url,headers=headers)
通过简单两行实现了对cookie的处理
p=v2exsession.post(url,data=postData,headers=headers)
对post方法的使用
'''
import re
import requests

#准备工作
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    "Referer": "http://www.v2ex.com/signin"
}
v2exsession=requests.Session()
url='https://www.v2ex.com/signin'
signin_data=v2exsession.get(url,headers=headers)

#用户名和密码的参数名字从网页中寻找
#构造pattern
pattern_user=re.compile('input type="text" class="sl" name="(.*?)" value="" autofocus=')
pattern_paword=re.compile('input type="password" class="sl" name="(.*?)" value="" autocorrect="off"')
pattern_once=re.compile('input type="hidden" value="(\d+)" name="once"')
#匹配相关数据并转字符串截取处理
hidden_id=pattern_once.findall(signin_data.text)
user=str(pattern_user.findall(signin_data.text))[2:-2]
paword=str(pattern_paword.findall((signin_data.text)))[2:-2]
once=str(hidden_id)[2:-2]
# print(user+password+test)

postData={
    user:'Vmap',
    paword:'password',
    'once': once,
    'next': '/',
}
# print(postData)
p=v2exsession.post(url,data=postData,headers=headers)
f=v2exsession.get('https://www.v2ex.com/settings',headers=headers)#访问是否成功
print(f.text)

