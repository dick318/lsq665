import requests
from loguru import logger
import time
import re
import execjs
import base64

sess = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}


def getJS():
    # 请求首页,
    r = sess.get('https://www.aqistudy.cn/historydata/daydata.php?city=%E6%9D%AD%E5%B7%9E&month=202109',
                 headers=HEADERS)
    logger.info(f'首页的状态码：{r.status_code}')
    text = r.text
    # 获取首页加载js的名字
    url = re.findall('<script type="text/javascript" src="(.*?)"></script>', text)[1]
    t = int(time.time())
    params = (
        ('v', str(t)),
    )
    # 请求获取js代码
    response = sess.get(f'https://www.aqistudy.cn/historydata/{url}', headers=HEADERS,
                        params=params)
    logger.info(f"请求js的状态码：{response.status_code}")
    eval_text = re.search(r'eval\((.*)\)', response.text).group(1)  # 返回一段js函数，去掉eval
    eval_text = execjs.eval(eval_text)  # 执行js获得base64加密后的js
    num = eval_text.count('dweklxde')  # 计算进行了几次base64，有0,1,2，三种情况
    if num != 0:  # 如果有进行base64加密
        eval_text = re.search(r"'(.*?)'", eval_text).group(1)  # 取出base64加密后的代码解密
        for i in range(num):
            eval_text = base64.b64decode(eval_text.encode()).decode()
        enc_func_name = re.search('if \(!(.*?)\)(.*?){(.*?)var (.*?)=(.*?)\((.*?)ajax', eval_text, re.S).group(
            5).strip()  # 获取加密函数的函数名
        dec_func_name = re.search('success: function \((.*?)\)(.*?)= (.*?)\(', eval_text, re.S).group(3) # 解密函数的函数名
        data_name = re.search('data: {(.*?):(.*?)}', eval_text).group(1).strip() # post请求时请求的参数名
    else:  # 生成的js没有加密
        enc_func_name = re.search('if\(!(.*?)\)\{var (.*?)=(.*?)\((.*?)ajax', eval_text).group(3).strip()
        dec_func_name = func_name = re.search('success:function\((.*?)\)(.*?)=(.*?)\(', eval_text).group(3)
        data_name = re.search('data:{(.*?):(.*?)}', eval_text).group(1).strip()
    # logger.info(data_name)
    # logger.info(enc_func_name)
    # logger.info(dec_func_name)
    # logger.info(eval_text)
    return data_name, enc_func_name, dec_func_name, eval_text


def getParames(func_name, text,query):
    # 根据解密出来的js与扣出来的静态js拼接执行
    node = execjs.get()
    with open('./1.js', 'r', encoding='utf-8') as f:
        ctx = node.compile(f.read() + text)
        sign = ctx.call(func_name, 'GETDAYDATA', query)
        # logger.info(sign)
        return sign, ctx


def decrypt(data, dec_func_name, ctx):
    # 解密请求的数据
    data = ctx.call(dec_func_name, data)
    logger.info(data)


def getEncryptData(data_name, sign):
    # 请求api获取加密的数据
    data = {}
    data[data_name] = sign
    response = sess.post('https://www.aqistudy.cn/historydata/api/historyapi.php', headers=HEADERS, data=data)
    logger.info(f"请求数据的状态码：{response.status_code}")
    # logger.info(response.text)
    return response.text


if __name__ == '__main__':
    query ={'city': '武汉', 'month': '201906'} # 查询参数
    data_naem, enc_func_name, dec_func_name, text = getJS()
    sign, ctx = getParames(enc_func_name, text,query)
    data = getEncryptData(data_naem, sign)
    decrypt(data, dec_func_name, ctx)
