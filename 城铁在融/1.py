import requests
import re
from  loguru import logger
import execjs

sess = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
}

def getPassword(password,key):
    with open('./1.js','r',encoding='utf-8 ') as f:
        node = execjs.get()
        js = node.compile(f.read())
        password = js.call('encryptByDES',password,key)
        logger.info(f'密码为：{password}')
        return password


def getKey():
    r = sess.get('http://www.ctzrnet.com/user/to_login',headers=headers)
    key = re.search(r'<input type="hidden" name="publickey" id="publickey" value="(.*?)" />',r.text).group(1)
    logger.info(f'publickey:{key}')
    return key

def login(password,key):
    data = {
      'account': '15222222222',
      'password': password,
      'publickey': key,
      'captcha': '5by4'
    }

    response = requests.post('http://www.ctzrnet.com/user/login', headers=headers, data=data, verify=False)
    print(response.text)

if __name__ == '__main__':
    key = getKey()
    password = getPassword('123456',key)
    login(password,key)