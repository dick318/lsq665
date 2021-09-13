import redis
import requests
from bs4 import BeautifulSoup
import time


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
}

url='https://s.weibo.com/top/summary?cate=realtimehot'

def getText(url):
    '''根据url返回对应的文本数据'''
    r=requests.get(url,headers=headers,timeout=5)
    print(r.status_code)
    soup=BeautifulSoup(r.text,'lxml')
    return soup


def analyzesText(soup,key='0'):
    '''解析数据'''
    # 创建一个空集合用来存放数据
    url_set=set()
    # 解析数据
    table=soup.find('table')
    tbody=table.find('tbody')
    tr_list=iter(tbody.find_all('tr'))
    # 舍弃第一条
    next(tr_list)
    for tr in tr_list:
        td2=tr.find('td',class_='td-02')
        # 获取热搜链接，有两种格式
        href1=td2.a.get('href')
        if href1 == 'javascript:void(0);':
            href1=td2.a.get('href_to')
        href='https://s.weibo.com'+ href1
        hotSearch=td2.a.text
        if key=='0':
            # 排名
            number = tr.find('td', class_='td-01 ranktop').text
            if number == '•':
                continue
            # 点击量
            dianji=td2.span.text
            # 标签
            td03=tr.find('td',class_='td-03').text
            # print(number,hotSearch,href,dianji,td03)
            # 做成字符串
            c = f'{number} {hotSearch} {href} {dianji} {td03}'
            url_set.add(c)
        else:
            print(hotSearch, href)
    return url_set

def main(instance):
    '''根据获得的数据进行分析'''
    with redis.Redis(host='127.0.0.1',port=6379,db=1,password='****') as client:
        # 新获得的数据
        new_url_set = analyzesText(getText(url))
        # 将新的数据中的url解析出来，用来作差集，求新增的热搜
        new_url_set1=set(map(lambda x:x.split(' ')[2],new_url_set))
        # 如果不是第一次
        if instance == 1:
            # 从数据库中取出上一次的数据
            old_url_set = set(map(lambda x: x.decode(), client.smembers('weibo')))
            # 将上一次的数据中的url解析出来，用来作差集，求新增的热搜
            old_url_set1 = set(map(lambda x: x.split(' ')[2], old_url_set))
            '''新增的热搜'''
            subtraction('新增',new_url_set1,old_url_set1,new_url_set)
            '''减少的热搜'''
            subtraction('减少',old_url_set1,new_url_set1,old_url_set)
        # 运行后的第一次。返回当前的50条热搜
        else:
            print('当前的微博热搜为：',time.ctime())
            y=list(new_url_set)
            # 排序
            y.sort(key=lambda x:int(x.split(' ')[0]))
            for i in y:
                print(i)
        # 删除原来的数据库中的数据
        client.delete('weibo')
        # 将新的数据写入数据库
        client.sadd('weibo',*new_url_set)

def subtraction(text,new_url_set1,old_url_set1,new_url_set):
    print(f'{text}的热搜为：(与一分钟前相比):',time.ctime())
    # 根据url作差集取出新增数据
    y=list(new_url_set1 - old_url_set1)
    # 根据作差集得到的数据获得完整的数据
    y=list(filter(lambda x:x.split(' ')[2] in y,new_url_set))
    # 根据排名排序
    y.sort(key=lambda x: int(x.split(' ')[0]))
    for i in y:
        print(i)





if __name__ == '__main__':
    # 第一次输出全部结果
    start = time.time()
    main(0)
    time.sleep(60 - (time.time() - start))
    while True:
        print('华丽的分割线'.center(100,'-'))
        start = time.time()
        main(1)
        time.sleep(60 - (time.time()-start))
