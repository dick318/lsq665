import requests
import time
import random
# from fake_useragent import UserAgent
from bs4 import BeautifulSoup

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.9171'}

# 请求页面，获取源码
def get_text(url):
    r=requests.get(url,headers=headers,timeout=5)
    r.encoding='utf-8'
    print(r.status_code)
    soup=BeautifulSoup(r.text,'lxml')
    return soup

soup=get_text('https://www.qidian.com/rank')
sopu=soup.find('div',class_='type-list')
list_url=sopu.find_all('a')
for ij in list_url:
    # 推荐票分周，月和总
    x = ['周:', '月:', '总:']
    x = iter(x)
    # 获取各小说种类的url
    url='https://www.qidian.com/rank?chn={}'.format(ij.get('data-chanid'))
    print(ij.text.center(100,'='))
    # 获取网页源码
    soup=get_text(url)
    soup11=soup.find_all(class_='rank-list')
    for soup1 in soup11:
        title=soup1.find('h3').text.replace('更多','')+':'
        print(title)
        li_div=soup1.find_all('div',class_='book-list')
        for i in li_div:
            ul=i.find('ul')
            li=ul.find_all('li')
            li_iter=iter(li)
            # 解析第一本书
            book1=next(li_iter)
            data_rid=book1.get('data-rid')
            href='https:'+ book1.find('a').get('href')
            name=book1.find('a').text
            piao=book1.find('p',class_='digital').text
            print(data_rid,name,href,piao)

            try:
                # 解析后面的书
                if title == '推荐票榜:':
                    print(next(x))
                for j in li_iter:
                    data_rid = j.get('data-rid')
                    href = 'https:'+ j.find('a').get('href')
                    name = j.find('a').text
                    try:
                        piao=j.find('i',class_='total').text
                    except:
                        piao='none'
                    print(data_rid,name,href,piao)
            except:
                print('none')
    time.sleep(1.5)