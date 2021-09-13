'''https://www.youzy.cn/tzy/search/colleges/collegeList'''


'''检查：Content-Length: 131，post请求提交的数据中不能有空格'''
'''线程池'''
import requests
import hashlib
import execjs
import json
import time
from concurrent.futures import ThreadPoolExecutor,as_completed

def get_token(data):
    # 1.实例化一个node对象
    # node = execjs.get()
    # path = r'js.js'
    # with open(path, 'r', encoding='utf-8') as f:
    #     # 2.js源文件编译
    #     ctx = node.compile(f.read())
    #     # 3.执行js函数
    #     funcName = f'x("/youzy.dms.basiclib.api.college.query",{data})'
    #     pwd = ctx.eval(funcName)
    #     # print(pwd)
    data=data+'&9SASji5OWnG41iRKiSvTJHlXHmRySRp1'
    data = data.lower()
    return hashlib.md5(data.encode()).hexdigest()


def get_data(i):
    data = {"keyword":"","provinceNames":[],"natureTypes":[],"eduLevel":"","categories":[],"features":[],"pageIndex":i,"pageSize":20,"sort":7}
    url = 'https://uwf7de983aad7a717eb.youzy.cn/youzy.dms.basiclib.api.college.query'
    data = json.dumps(data).replace(' ','')
    headers = {'Host': 'uwf7de983aad7a717eb.youzy.cn', 'Connection': 'keep-alive', 'Content-Length': '131', 'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 'u-token': '', 'sec-ch-ua-mobile': '?0', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Content-Type': 'application/json', 'Accept': '*/*', 'Origin': 'https://pv4y-pc.youzy.cn', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://pv4y-pc.youzy.cn/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'u-sign': get_token(data)}
    r = requests.post(url=url,headers=headers, data=data,verify = False)
    print(r.status_code)
    school = r.json()['result']['items']
    namelist = list(map(lambda x:x.get('cnName'),school))
    return namelist



if __name__ == '__main__':
    start = time.time()
    with ThreadPoolExecutor(10) as pool:
        future_list =[pool.submit(get_data,i) for i in range(140,147)]
        x = [j.result() for j in future_list]
        print('用时：',time.time()-start)
        y = sum(x,[])
        for i in y:
            print(i)
        print(y.index('武汉纺织大学'))

