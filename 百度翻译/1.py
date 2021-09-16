import requests
import execjs
import re
import time
from loguru import logger
import math

sess = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
}


def getSign(gtk, data):
    def a(r):
        try:
            result = r if isinstance(r, list) else list(r)
        except:
            result = []
        return result

    def n(r, o):
        for t in range(0, len(o) - 2, 3):
            a = o[t + 2]
            if a >= "a":
                a = ord(a[0]) - 87
            else:
                a = int(a)
            if o[t + 1] == '+':
                a = r >> a
            else:
                a = r << a
            if o[t] == '+':
                r = r + a & 4294967295
            else:
                r = r ^ a
        return r

    def e(r):
        # o = re.search('[\uD800 -\uDBFF][\uDC00 -\uDFFF]', r).group()
        o = None
        if o == None:
            t = len(r);
            if t > 30:
                length = math.floor(t / 2 - 5)
                r = "" + r[0:10] + r[length: length + 10] + r[-10:]
            else:
                pass
            u, l = '', 'gtk'
            u = i = gtk
            d = u.split(".")
            m = int(d[0]) or 0
            s = int(d[1]) or 0
            S = [-1] * 100
            c = 0
            for v in range(len(r)):
                A = ord(r[v])
                if 128 > A:
                    S[c] = A
                    c += 1
                else:
                    if A < 2048:
                        S[c] = A >> 6 | 192
                        c += 1
                    else:
                        if 55296 == (64512 & A) and v + 1 < r.length and 56320 == (64512 & r.charCodeAt(v + 1)):
                            # v += 1
                            A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v))
                            S[c] = A >> 18 | 240
                            c += 1
                            S[c] = A >> 12 & 63 | 128
                            c += 1
                        else:
                            S[c] = A >> 12 | 224
                            c += 1
                            S[c] = A >> 6 & 63 | 128
                            c += 1
                    S[c] = 63 & A | 128
                    c += 1
            S = list(filter(lambda x: x != -1, S))
            p = m
            # F = "" + chr(43) + chr(45) + chr(97) + ("" + chr(94) + chr(43) + chr(54))
            # D = "" + chr(43) + chr(45) + chr(51) + ("" + chr(94) + chr(43) + chr(98)) + ("" + chr(43) + chr(45) + chr(102))
            F = '+-a^+6'
            D = '+-3^+b+-f'
            for b in range(len(S)):
                p += S[b]
                p = n(p, F)
            p = n(p, D)
            p ^= s
            if 0 > p:
                p = (2147483647 & p) + 2147483648
            p %= 1e6
            return str(int(p)) + "." + str(int(p) ^ int(m))

    return e(data)

def getCookie():
    '''请求获取返回的cookie'''
    sess.get('https://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh',
             headers=headers)


def getParames(data):
    # 请求首页获取加密的gtk和token
    url = 'https://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh'
    r = sess.get(url,headers=headers)
    logger.info(r.status_code)
    text = r.text
    gtk = re.search("window.gtk = '(.*?)';",text).group(1).strip()
    token = re.search("token: '(.*?)'",text).group(1).strip()
    logger.info(f"gtk:{gtk!r},token:{token!r}")
    # 根据gtk和要翻译的内容计算sign
    # node = execjs.get()
    # with open('./1.js', 'r', encoding='utf-8') as f:
    #     # 2.js源文件编译
    #     ctx = node.compile(f.read())
    #     pwd = ctx.call("getSign", gtk, data)
    #     logger.info(pwd)
    pwd = getSign(gtk,data)
    return token,pwd


def getmessage(query):
    getCookie() # 获取cookie
    token,sign = getParames(query) # 获取请求参数
    params = (
        ('from', 'en'),
        ('to', 'zh'),
    )

    data = {
        'from': 'en',
        'to': 'zh',
        'query': query,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': sign,
        'token': token,
        'domain': 'common'
    }

    response = sess.post('https://fanyi.baidu.com/v2transapi', headers=headers, params=params,
                             data=data)

    logger.info(response.status_code)
    logger.info(response.json()["trans_result"]['data'][0]['dst'])


if __name__ == '__main__':
    start = time.time()
    getmessage('hello world')
    logger.info(f'耗时：{time.time()-start}')
