'''https://www.kanzhun.com/'''
import requests
import execjs
import re
from bs4 import BeautifulSoup
from loguru import logger

node = execjs.get()
f = open('1.js', 'r', encoding='utf-8')
ctx = node.compile(f.read())
f.close()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'cookie': '__a=365143',
}


def getID(url):
    response = requests.get('https://www.kanzhun.com' +url, headers=headers)
    text =  response.text
    id = re.search(r'pdata="\{p1:(.*?)\}',text).group(1)
    title = re.search(r'<strong>(.*?)</strong>',text).group(1)
    logger.info(title)
    return id


def encryptData(argument):
    password = ctx.call('get1_data', argument)
    logger.info(password)
    return password


def decryptData(data):
    password = ctx.call('get_data', data)
    print(password)


def getData(id):
    # 获取一些详细信息
    params = (
        ('b', encryptData('{"encCompanyId":"%s","questionId":"","optionId":""}' % (id))),
        ('kiv', 'YmgMtXlZeqN8VLEu'),
    )
    response = requests.get('https://www.kanzhun.com/api_to/webquestion/publish.json', headers=headers, params=params)
    text = response.text
    logger.info(f'第一次请求的结果：{text}')
    decryptData(text)

    params = (
        ('b', encryptData('{"pageType":4,"encCompanyId":"%s"}' % (id))),
        ('kiv', 'YmgMtXlZeqN8VLEu'),
    )
    response = requests.get('https://www.kanzhun.com/api_to/statement/index.json', headers=headers, params=params)
    text = response.text
    logger.info(f'第2次请求的结果：{text}')
    decryptData(text)
    '''薪资'''
    # /api_to/salary_chart/chart.json
    # '{"encCompanyId":"0nJ42dm8EQ~~","type":0}'
    params = (
        ('b', encryptData('{"encCompanyId":"%s","type":0}' % (id))),
        ('kiv', 'YmgMtXlZeqN8VLEu'),
    )
    response = requests.get('https://www.kanzhun.com/api_to/salary_chart/chart.json', headers=headers, params=params)
    text = response.text
    logger.info(f'第3次请求的结果：{text}')
    decryptData(text)

    # /api_to/com_salary_v2/list.json
    # {"encCompanyId":"0nJ42dm8EQ~~","cityCode":"","positionCode":"","pageNum":1,"sortMethod":0}

    params = (
        ('b', encryptData('{"encCompanyId":"%s","cityCode":"","positionCode":"","pageNum":1,"sortMethod":0}' % (id))),
        ('kiv', 'YmgMtXlZeqN8VLEu'),
    )
    response = requests.get('https://www.kanzhun.com/api_to/com_salary_v2/list.json', headers=headers, params=params)
    text = response.text
    logger.info(f'第4次请求的结果：{text}')
    decryptData(text)

    '''风险'''
    #/api_to/cer/list.json
     # 文书
    params = (
        ('b', encryptData('{"encCompanyId":"%s"}' % (id))),
        ('kiv', 'YmgMtXlZeqN8VLEu'),
    )
    response = requests.get('https://www.kanzhun.com/api_to/cer/list.json', headers=headers, params=params)
    text = response.text
    logger.info(f'第5次请求的结果：{text}')
    decryptData(text)
    # 公告
    response = requests.get('https://www.kanzhun.com/api_to/cer/list_v2.json', headers=headers, params=params)
    text = response.text
    logger.info(f'第6次请求的结果：{text}')
    decryptData(text)

def getLink():
    url = 'https://www.kanzhun.com/msh/?ka=index-icon-click'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    links = map(lambda x: x.get('href'), soup.select('[ka="view_list_interview_title"]'))
    return links

if __name__ == '__main__':
    links = getLink()
    for url in links:
        id = getID(url)
        getData(id)
        print('华丽的分割线'.center(100, '-'), end='\n\n\n\n')
