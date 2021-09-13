'''http://www.chinapesticide.org.cn/myquery/queryselect'''
'''农药登记数据'''

import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

async def get_text(i):
    url='http://www.chinapesticide.org.cn/myquery/queryselect'
    print('开始请求第{}页'.format(i))
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    data={'pageNo': f'{i}', 'pageSize': '30', 'djzh': '', 'nymc': '', 'cjmc': '', 'sf': '', 'nylb': '', 'zhl': '', 'jx': '', 'zwmc': '', 'fzdx': '', 'syff': '', 'dx': '', 'yxcf': '', 'yxcf_en': '', 'yxcfhl': '', 'yxcf2': '', 'yxcf2_en': '', 'yxcf2hl': '', 'yxcf3': '', 'yxcf3_en': '', 'yxcf3hl': '', 'yxqs_start': '', 'yxqs_end': '', 'yxjz_start': '', 'yxjz_end': ''}
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url,data=data,headers=headers) as r:
            # print(r.status)
            print(r.status)
            text = await r.text()
            soup = BeautifulSoup(text,'lxml')
            div = soup.find('div',class_='web_ser_body_right_main_search')
            table =div.find('table',recursive=False)
            tr_list = table.find_all('tr')
            return tr_list[-1].text.replace('\n',' ')

async def main():
    tasks = [asyncio.create_task(get_text(i)) for i in range(1,10)]
    for i in asyncio.as_completed(tasks):
        result = await i
        print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
