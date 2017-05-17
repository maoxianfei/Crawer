#!/usr/bin/env python
# encoding: utf-8
import requests
import re
import os
import time
import urllib.request
#according the current time to create file and put the downloaded pictures into the directory
def createFile():  
    global path #we need path when downloading picture,so we set path as a global variable in advance
    filetime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    path = './flower_beauty/' + filetime
    if not os.path.exists('./flower_beauty'):
        os.mkdir('./flower_beauty')
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def downloadimg(key,path):
    #The key is a list,when a list convert to a str keeps [''],it should use [2:-2] to filter
    imgurl='https://hbimg.b0.upaiyun.com/'+str(key)[2:-2]+'_fw658'   
    urllib.request.urlretrieve(imgurl,path+'/'+str(key)[2:-2]+'.jpg')
    # print(imgurl)

#If the filename include unvalid character like '/\:*<>|"?' will led to create file failed
def validname(title):
    rstr='[\/\\\:\*\?\"\<\>\|]'
    valid_title=re.sub(rstr,'',title)
    return valid_title
 
def get_img_key(id):
    #得到图片id
    home_url='https://huaban.com/pins/'
    url=home_url+str(id)+'/'
    webdata=requests.get(url)
    data=webdata.text
    #数据筛选找到key
    firstRE = re.compile(r'app\["page"\](.*?), "text_meta"')
    firstdata = firstRE.findall(data)
    # print(firstdata)
    key=re.findall('"key":"(.*?)"',str(firstdata))
    # print(key)
    return key

    #对key构造地址
#749a992fb659e939ebc4f5690da60a81fed54c405068e-Illc20_fw658
    # with open('./tempdata.txt','w',encoding='utf-8') as tempw:
    #     tempw.write(data)
    #     tempw.close()
    # with open('./tempdata.txt','r+',encoding='utf-8') as tempr:
    #     data1=tempr.read()
    #     picurl = picRE.findall(data1,re.S)
    #     print(picurl)
    #     tempr.close()
# def get_img_id():
    # web_data=requests.get("https://huaban.com/favorite/beauty/")

def get_id(beauty_url):
    web_data = requests.get(beauty_url)
    pinRE = re.compile('"pin_id":(\d*?), "user_id":\d*?,')
    pinid = pinRE.findall(web_data.text)
    # a=0
    # for id in pinid:
    #     get_img(id)
    #     a+=1
    #     print("第{}个".format(a))
    return pinid

def unique_id(id_list):
    id_list=list(set(id_list))
    return id_list

def get_next(beauty_url='https://huaban.com/favorite/beauty/'):
    id_list = get_id(beauty_url)[:]  # 解析页面当前的id
    id_set = list(set(id_list))
    id_list_uniqune = unique_id(id_list)  # 对id列表去重
    # print(id_list_uniqune)
    #循环下载函数
    count=0
    for id in id_list_uniqune:
        count+=1
        key = get_img_key(id)  # 通过id得到key
        downloadimg(key, path)  # 通过key和path下载文件
        print("download {}".format(count))
        # if count>5:
        #     break
    return id_list[-1]
'''
198368485', '918789198', '198369677', '198363750', '350010205',
'670115744', '172796713', '898076056', '917512201', '313298032',
'918586402', '918920381', '525798891', '313304628', '918079727',
'564055088', '898132640', '918784856', '917512519', '212946705',
'918894995', '303222393', '904194691', '918944339', '918955317',
'217881447', '350010146', '898133035', '198375016', '344794002',
'898133172', '855305051', '918917448', '918978911', '918780514',
'917512027', '918957316', '898132699', '918079809', '296216360', '
394382196', '218761604', '670115745', '918991904', '670115742',
'918944392', '917393726', '388327469', '346550851', '918973592',
'918901743', '917511868', '313303957', '898133006', '313303569',
'299703741', '204765314', '917395347', '918956902', '918788348',
'206411589', '918081274', '802643792', '918896254', '670115743',
'670115740', '918081360', '296218662', '918994440', '918585230',
'913841090', '823423111', '918915500', '346550562', '383143365',
'898133053', '918979535', '670115748', '802683220', '670115749',
'898132715', '898133143', '346550402', '670115751', '802643684',
'313295155', '297719115', '917511136']
https://huaban.com/favorite/beauty/?ivhdm0s5&max=914688397&limit=20&wfl=1
'''
if __name__ == '__main__':
    # list1=get_next(beauty_url='https://huaban.com/favorite/beauty/')
    # list2=get_next(beauty_url='https://huaban.com/favorite/beauty/?ivhdm0s5&max=914688397&limit=20&wfl=1')
    # for li1 in list1:
    #     if li1 in list2:
    #         print("double {}".format(li1))
    #     else:
    #         print("none")
    path=createFile()
    pages=100
    last_id=get_next()
    #this loop control the download pages
    for page in range(1,pages):
        beauty_url = 'https://huaban.com/favorite/beauty/?ivhdm0s5&max={}&limit=20&wfl=1'.format(last_id)
        last_id=get_next(beauty_url)









