from tkinter import *
from tkinter.ttk import *
# from movice import Search_main
import requests,re,json
from bs4 import BeautifulSoup
headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}


def search_pansou(query_key):
    url = 'http://api.pansou.com/search_new.php?q=%s' % query_key.decode('utf-8')

    j = requests.get(url=url, headers=headers).json()

    if j['listcount'] > 0:
        items = j['list']['data']
        if items:
            return [item['link'] for item in items if item['host'] == 'pan.baidu.com']
        else:
            return None
    else:
        return None


def bsou(query_key):
    headers['Origin'] = 'http://www.xilinjie.com'
    url = 'http://116.62.9.6:8081/?q=%s' % query_key.decode('utf-8')

    r = requests.get(url=url, headers=headers)
    result_list = []
    try:
        for x in r.json()['hits']['hits']:
            source = x['_source']
            if source['domain'] == 'pan.baidu.com':
                result_list.append(source['url'])
    except Exception as e:
        pass

    return result_list


def search_huhupan(query_key):
    search_url = 'http://huhupan.com/e/search/index.php'
    data = {
        'keyboard': query_key,
        'show': 'title',
        'tempid': 1,
        'tbname': 'news',
        'mid': 1,
        'dopost': 'search'
    }
    r = BeautifulSoup(requests.post(url=search_url, headers=headers, data=data).content, 'lxml')
    items_list = r.find_all('span', {'class': 'more'})

    yunpan_href = []

    if items_list:
        for item in set(items_list):
            temp_href = huhupan_url(item.find('a')['href'])
            if temp_href:
                yunpan_href.extend(temp_href)
    else:
        return None

    return yunpan_href


def huhupan_url(url):
    r = BeautifulSoup(requests.get(url=url, headers=headers).content, 'lxml')
    baiduyun_href = r.find('a', {'class': 'meihua_btn', 'href': re.compile(r'/e/extend/down/.*')})

    if baiduyun_href:
        baiduyun_url = 'http://huhupan.com' + baiduyun_href['href']
        yunpan_href = parse_huhupan(baiduyun_url)

        if yunpan_href:
            return yunpan_href
        else:
            return None
    else:
        return None



def parse_huhupan(url):
    r = BeautifulSoup(requests.get(url=url, headers=headers).content, 'lxml')
    href_list = r.find_all('a', {'class': 'meihua_btn', 'href': re.compile(r'http://pan\.baidu\.com/.*')})
    pwd_list = r.find_all('input', {'id': re.compile(r'foo[0-9]')})

    if pwd_list:
        return ['链接:{},密码:{}'.format(href_list[x]['href'], pwd_list[x]['value']) for x in range(len(href_list))]
    else:
        return None


def search_movice(keyword):
    query_key = keyword
    l = []

    try:
        huhupan_result = search_huhupan(query_key)
        if huhupan_result:
            l.extend(huhupan_result)
    except:
        pass

    try:
        bsou_result = bsou(query_key)
        if bsou_result:
            l.extend(bsou_result)
    except:
        pass

    return l

def Search_main(keyword):
    wrong_return = u'暂未找到 [%s] 相关的百度云资源，回复电影名称的关键词试试。\n\n比如想看电影一个叫欧维的男人决定去死，可以回复关键词 [欧维] 或者 [一个叫] 等等。' % keyword

    try:
        result_list = search_movice(keyword.encode('utf-8'))
        if result_list:
            return u'搜索电影[%s]的百度云资源如下:\r\n' % keyword + '\r\n'.join(result_list)
        else:
            return wrong_return
    except:
        return wrong_return


#GUI
def serach_key():
    keys=input_text.get()
    show_text.delete(1.0,END)
    result=Search_main(keys)
    show_text.insert(1.0,result)
    # print(result)

root=Tk()#实例化
root.wm_title('百度资源搜索器v1.0_Richard Mao')#设置标题
root.geometry("500x400+600+200")#width x height + x+y
root.resizable(width = False, height = False)#不能修改界面长宽

label_show=Label(root,text='输入资源关键词(点击按钮后请等待几秒)')
label_show.pack()

input_text=Entry(root,text="please input",width=50)
input_text.pack()
seaech_button=Button(root,text='Search',command=serach_key)
seaech_button.pack()
show_text=Text(root)
show_text.pack()
root.mainloop()#23vbnm