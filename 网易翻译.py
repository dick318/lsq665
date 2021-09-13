# import urllib.request as ur
# import urllib.parse as up
import requests
import json
import hashlib
import time
import random

count = input('请输入要翻译的内容：')

# url
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

# 请求头，字典
head={}
head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.9171'

ti=str(int(time.time()*1000))
ti1 = ti + str(random.randint(0,9))
print(ti1)
sign=hashlib.md5(('fanyideskweb'+count+ti1+'Tbh5E8=q6U3EXe+&L[4c@').encode()).hexdigest()
bv = hashlib.md5(head.get('User-Agent')[8:].encode()).hexdigest()
print(bv)


# post 请求，字典
data = {'i': count,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': ti1,
        'sign': sign,
        'lts': ti,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION'}


r =requests.post(url,data=data,headers=head)
print(r.status_code)

print(r.headers)
html=r.text

print(html)
html = json.loads(html)
html = html['translateResult'][0][0]['tgt']
print(html)
