'''http://guba.eastmoney.com/rank/'''

import requests
import time
import execjs
import re
import json

t = str(time.time() * 1000)[:13]

def get2(url):
    url =url+ f'&cb=qa_wap_jsonpCB{t}'
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'push2.eastmoney.com',
               'Pragma': 'no-cache',
               'Referer': 'http://guba.eastmoney.com/',
               'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
               'sec-ch-ua-mobile': '?0',
               'Sec-Fetch-Dest': 'script', 'Sec-Fetch-Mode': 'no-cors', 'Sec-Fetch-Site': 'cross-site',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    return json.loads(r.text.strip()[28:-2])

def get1(page=1):
    url = f'http://gbcdn.dfcfw.com/rank/popularityList.js?sort=0&page={page}&_={t}'
    headers = {
        'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'gbcdn.dfcfw.com', 'Pragma': 'no-cache',
        'Referer': 'http://guba.eastmoney.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    r = requests.get(url,headers=headers)
    print(r.status_code)
    # 替换多余的部分只要响应数据
    data = r.text.replace('var popularityList=','').strip('\'')

    node = execjs.get()
    with open('./1.js', 'r', encoding='utf-8') as f:
        # 2.js源文件编译
        ctx = node.compile(f.read())
        # 3.执行js函数
        funcName = 'get_data("{0}")'.format(data)
        pwd = ctx.eval(funcName) # 第一个请求返回的解析后的数据
        # 计算第二次请求的参数
        e = ','.join(re.findall('"code":"(.*?)"',pwd))
        url2 = ctx.eval(f'getLink("{e}")')
        return json.loads(pwd),url2

def main():
    with open('./1.csv','w',encoding='utf-8') as f:
        field = '日期,当前排名,排名变动,代码,股票名称,最新价,涨跌额,涨跌幅'
        print(field,)
        print(field,file=f)
        for page in range(1,6):
            data1, url2 = get1(page)
            data2 = get2(url2)['data']['diff']
            for i in range(len(data1)):
                date = data1[i].get("exactTime")
                rankNumber = data1[i].get("rankNumber")
                changeNumber = data1[i].get("changeNumber")
                code = data1[i].get("code")
                ironsFans = data1[i].get("ironsFans")
                newFans = data1[i].get("newFans")
                name = data2[i].get("f14")
                new_price = data2[i].get("f2")
                upsAndDowns = data2[i].get("f4") # 涨跌额
                quoteChange = data2[i].get("f3") # 涨跌幅
                print(date, rankNumber, changeNumber, code, name, new_price, upsAndDowns, quoteChange,sep=',')
                print(date,rankNumber,changeNumber,code,name,new_price,upsAndDowns,quoteChange,sep=',',file=f)






if __name__ == '__main__':
    main()