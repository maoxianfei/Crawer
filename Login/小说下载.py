#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
 *                             _ooOoo_
 *                            o8888888o
 *                            88" . "88
 *                            (| -_- |)
 *                            O\  =  /O
 *                         ____/`---'\____
 *                       .'  \\|     |//  `.
 *                      /  \\|||  :  |||//  \
 *                     /  _||||| -:- |||||-  \
 *                     |   | \\\  -  /// |   |
 *                     | \_|  ''\---/''  |   |
 *                     \  .-\__  `-`  ___/-. /
 *                   ___`. .'  /--.--\  `. . __
 *                ."" '<  `.___\_<|>_/___.'  >'"".
 *               | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *               \  \ `-.   \_ __\ /__ _/   .-` /  /
 *          ======`-.____`-.___\_____/___.-`____.-'======
 *                             `=---='
 *          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 *                     佛祖保佑        永无BUG
'''
import re
import os
import requests
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
import smtplib

def Query(url):
    '''
    查询小说目录
    :param url:小说目录链接
    :return:小说目录列表类型 [链接，章节名称]
    '''
    webdata=requests.get(url+'index.html')
    webdata.encoding='gbk'
    pattern=re.compile('<dd><a href="(.*?)">(.*?)</a></dd>')
    li=pattern.findall(webdata.text)
    li[:]=[list(c) for c in li]
    for i in li:
        i[0]=url+i[0]
        # print(i)
    print('-------------------\n共%d节内容' % len(li))
    print('最新章节：%s \n-------------------'%li[-1][1])
    return li
def Createfile(bookname='novel'):
    '''
    创建文件夹和文本文件
    :param bookname:
    :return:
    '''
    path ='./book/'+bookname+'.txt'
    if not os.path.exists('./book'):
        os.mkdir('./book')
        print("Create book floder success")
    if not os.path.exists(path):
        with open(path, 'w') as d:
            d.write('test begin\n')
    return path

def Download(url_chapter,chapter,bookname='novel'):
    '''
    下载章节内容
    :param url_chapter: 每一章节的url
    :param chapter: 章节名称
    :param bookname: 小说名称
    :return:
    '''
    page=requests.get(url_chapter)
    page.encoding='gbk'
    print('状态码：',page.status_code)
    pattenr=re.compile('<!--go-->(.*)<!--over-->',re.S)#换行匹配
    page_text=pattenr.findall(page.text)
    Chinese="[^\u4e00-\u9fa5，]"#替换除了中文字符和逗号的所有字符
    page_text1=re.sub(Chinese,'',str(page_text))
    with open('./book/'+bookname+'.txt', 'a+') as f:
        f.write(chapter)
        f.write('\n')
        f.write(str(page_text1))
        f.write('\n')
def Choose(url,bookname='novel',start_num=0,end_num=-1,):
    '''
    输入目录链接开始下载从第几章到第几章内容
    :param url: 小说目录链接
    :param start_num: 开始章节（默认为最开始，列表序号起始为0）
    :param end_num: 终止章节（默认为最后）
    :return:path,最新章节
    '''
    path=Createfile(bookname)
    downloadlist=Query(url)
    chapter_size=len(downloadlist)
    # print('download from chapter 《%s》 to 《%s》'%(downloadlist[start_num][1],downloadlist[end_num][1]))
    i = start_num
    while i<chapter_size:
        url_chapter=downloadlist[i][0]
        chapter=downloadlist[i][1]
        print(url_chapter,chapter)
        Download(url_chapter,chapter,bookname)
        i=i+1
    latest=downloadlist[end_num][1]
    print('>>>download done')
    return path,latest
def Duplicate(tmp):
    patterns = []
    for line in tmp.split("\n"):
        if line not in patterns:
            # print('line=',line)
            patterns.append(line)
    print("pattern",patterns)
    sum=''
    for patt in patterns:
        sum=sum+patt+'\n'
    # print('sum='+sum)
    return sum
def email(path,head):
    '''
    发送邮件给
    :param path: 附件路径
    :param head: 邮件主题
    :return:
    '''
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    from_addr = '@163.com'
    password = 'bdxztldobaorgfag'
    to_addr = ''
    smtp_server = 'smtp.qq.com'
    # msg = MIMEText('hello', 'plain', 'utf-8')
    msg=MIMEMultipart()
    msg['From'] = _format_addr('小说爬虫程序 <%s>' % from_addr)
    msg['To'] = _format_addr('我的Kindle <%s>' % to_addr)
    msg['Subject'] = Header(head, 'utf-8').encode()

    #邮件正文
    msg.attach(MIMEText('hello', 'plain', 'utf-8'))
    #邮件附件
    with open(path,'rb')as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('text', 'txt', filename=path.split('/')[-1])
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=path.split('/')[-1])
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print('send mail success')
    except:
        print('send mail fail')
def getconfig(head):
    '''
    :param head: 读取小说存储记录
    :return: 返回记录（str）
    '''
    if not os.path.exists('./update.ini'):
        open('./update.ini', 'w+')
    with open('./update.ini','r') as r:
        tmp=r.read()
        a=re.findall(head+'=(.*)',tmp)
    print('>>>getconfig done')
    try:
        return a[0]
    except IndexError:
        return -1

def writeconfig(head,page):
    '''
    :param head: 写入小说名字
    :param page: 写入最新章节，如果重复则覆盖，没有则添加到末尾
    :return:
    '''
    page=str(page)
    if not os.path.exists('./update.ini'):
        open('./update.ini', 'w+')
    with open('./update.ini','r+') as f:
        tmp=f.read()
        tmp1=re.sub(head+'='+'\d+',head+'='+page,tmp)
        if tmp1==tmp:
            print('没有记录，添加内容')
            with open('./update.ini', 'a+') as f:
                f.write(head + '=' + page)
            with open('./update.ini', 'r') as f:
                dup=f.read()
            with open('./update.ini', 'w') as f:
                dup2=Duplicate(dup)
                print(dup2)
                f.write(dup2)
        else:
            print('有记录,修改原记录')
            with open('./update.ini', 'w+') as f:
                f.write(tmp1)
    print('>>>write config done')
def main():
    url={'Poor Rise':'http://www.aiquxs.com/read/46/46745/',
        'Legend of dragon king':'http://www.aiquxs.com/read/67/67831/',
    'Poor Champion':'http://www.aiquxs.com/read/46/46800/',}
    name={'1':'Poor Rise',
          '2': 'Legend of dragon king',
          '3': 'Poor Champion'
    }
    num=input('''-------------------
选择下载的小说序号
1---Poor Rise
2---Legend of dragon king
3---Poor Champion\n-------------------\n''')
    li=Query(url[name[num]])
    page_index=len(li)-1
    page=getconfig(name[num])
    if page==-1:
        page=input("请输入下载的起始章节:\n")
    path,head=Choose(url[name[num]],name[num],int(page))
    writeconfig(name[num],page_index)
    email(path,head)
if __name__=='__main__':
    main()
