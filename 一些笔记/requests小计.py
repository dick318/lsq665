'''-i https://pypi.tuna.tsinghua.edu.cn/simple'''
'''pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent'''

'''http://httpbin.org/get   http://httpbin.org/postt 测试网址'''
import requests

'''参数'''

# 请求头
'''http://useragentstring.com/pages/useragentstring.php?name=All'''
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "https://10.10.1.10:1080",
} # 代理
params = {'key1': 'value1',
          'key2': 'value2'} # 请求参数
files = {'file': open('report.xls', 'rb')}
cookies={}
# allow_redirects 参数禁用重定向处理
# verify=False 避免ssl认证       requests.exceptions.SSLError
auth=('username','password') # 身份认证
'''请求方式'''
r = requests.get(url='链接', params='构建链接的参数', headers='请求头', proxies='代理ip'
                 , cookies=cookies, timeout='响应时间', allow_redirects=False,verify=False,auth=auth)
r = requests.post(url='', data='', headers='请求头', proxies='代理ip', timeout='响应时间',files=files)

r = requests.put('http://httpbin.org/put', data={'key': 'value'})
r = requests.delete('http://httpbin.org/delete')
r = requests.head('http://httpbin.org/get')
r = requests.options('http://httpbin.org/get')

'''查看请求头'''
r.request.headers
'''响应类型'''
r.status_code  # 响应状态码
'''
101 - 申请跟换协议，websocket
200 - 请求成功，已经正常处理完毕
301 - 请求永久重定向，转移到其它URL
302 - 请求临时重定向
304 - 请求被重定向到客户端本地缓存
400 - 客户端请求存在语法错误
401 - 客户端请求没有经过授权
403 - 客户端的请求被服务器拒绝，一般为客户端没有访问权限
404 - 客户端请求的URL在服务端不存在
500 - 服务端永久错误
'''
r.encoding  # 文本编码
r.encoding = 'utf-8-sig'  # 修改文本编码
r.text  # 字符串形式的响应体
r.content  # 字节形式的响应体
r.json()  # 内置json解码器
r.history # 可以使用响应对象的 history 方法来追踪重定向
r.headers  # 响应头
r.cookies # 响应头设置的cookie set-cookie
r.cookies.get_dict() # 将cookie返回对象变为一个字典
r.cookies.items() # [(name,value),()]


'''会话对象让你能够跨请求保持某些参数,会话对象具有主要的 Requests API 的所有方法,不过需要注意，就算使用了会话，方法级别的参数也不会被跨请求保持'''
s = requests.Session()
s.headers={}  # 会话的请求头会保持请求头的顺序
s.cookies.set('key','value')
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
print(r.text)
# '{"cookies": {"sessioncookie": "123456789"}}'

'''Requests支持流式上传，这允许你发送大的数据流或文件而无需先把它们读入内存。要使用流式上传，仅需为你的请求体提供一个类文件对象即可：'''
with open('massive-body') as f:
    requests.post('http://some.url/streamed', data=f)


url=''
data={}
'''有时候你会碰到一些服务器，处于某些原因，它们允许或者要求用户使用上述 HTTP 动词之外的定制动词。比如说 WEBDAV 服务器会要求你使用 MKCOL 方法
。别担心，Requests 一样可以搞定它们。你可以使用内建的 .request 方法'''
r = requests.request('MKCOL', url, data=data)
r.status_code



import json
# json转换为python格式
json.loads()
# python转换为json格式
json.dumps()

import demjson
demjson.decode()
demjson.encode()


