'''https://gkcx.eol.cn/school/30/provinceline'''
'''2021-6-4'''
import requests
import execjs
import json
from urllib.parse import urlencode, unquote
import hmac
import base64
from hashlib import sha1, md5, sha256

'''
f = v.default.enc.Utf8.parse(f)  将f转换为二进制
f = v.default.HmacSHA1(f, "D23ABC@#56"),  将fhmacsha1后返回二进制摘要
f = v.default.enc.Base64.stringify(f).toString()  base64加密
'''
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}


def main():
    data = {'access_token': '',
            'local_province_id': '42',
            'local_type_id': '1',
            'page': '1',
            'school_id': '1316',
            'size': '10',
            'uri': 'apidata/api/gk/score/province',
            'year': ''}
    content = f'api.eol.cn/gkcx/api/?local_province_id={data["local_province_id"]}&' \
              f'local_type_id={data["local_type_id"]}&page=1&school_id={data["school_id"]}&' \
              f'size=10&uri=apidata/api/gk/score/province&year='
    sig = get_signsafe(content)
    data['signsafe'] = sig
    decrypt_data(data)


def hmacSha1(content) -> bytes:
    '''hmacSha1加密'''
    key = 'D23ABC@#56'.encode()
    # htx = hmac.new(key=key,msg=content.encode(),digestmod=sha1)
    # return htx.hexdigest()  # 十六进制摘要
    hmac_code = hmac.new(key, content.encode(), sha1).digest()
    return hmac_code


def get_signsafe(content):
    a = hmacSha1(content)
    # c = base64.b64encode(a).decode()
    # return md5(c.encode()).hexdigest()
    c = base64.b64encode(a)
    return md5(c).hexdigest()


def decrypt_data(data):
    r = requests.post('https://api.eol.cn/gkcx/api/', data=data, headers=headers)
    # print(r.status_code)
    if r.status_code == 200:
        encrypt_data = r.json()['data']['text']
        node = execjs.get()
        path = r'./aes.js'
        with open(path, 'r', encoding='utf-8') as f:
            # 2.js源文件编译
            ctx = node.compile(f.read())
            # 3.执行js函数
            funcName = 'get_data("{0}")'.format(encrypt_data)
            pwd = ctx.eval(funcName)
            print(pwd)
    else:
        print(r.status_code)

if __name__ == '__main__':
    import time
    start = time.time()
    main()
    print(time.time()-start)