'''http://jzsc.mohurd.gov.cn'''
import execjs
import requests
import os


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
# p_url = 'http://jzsc.mohurd.gov.cn/api/webApi/visits/count/incrSitePv'
#
# r=requests.get(url=p_url,headers=headers)
# print(r.text)

url='http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg=1&pgsz=15&total=450'

r=requests.get(url,headers=headers)
print(r.status_code)
print(r.text)
encrypt_data = r.text

'''js.js'''
def getPd():
    node = execjs.get()
    with open('js.js','r',encoding='utf-8') as f:
        ctx = node.compile(f.read())
        password = ctx.eval(f'h("{encrypt_data}")')
        print(password)
'''js1.js'''
# def getPd():
#     node = execjs.get()
#     with open('js1.js','r',encoding='utf-8') as f:
#         ctx = node.compile(f.read())
#         password = ctx.eval(f'get_data("{encrypt_data}")')
#         print(password)

getPd()