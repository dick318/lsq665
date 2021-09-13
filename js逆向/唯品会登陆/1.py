import requests
import execjs
from loguru import logger

url = 'https://passport.vip.com/login/postLogin'


def getPd():
    node = execjs.get()
    with open('js.js', 'r', encoding='utf-8') as f:
        ctx = node.compile(f.read())
        password = ctx.eval(f'getFromData("1111111111","e10adc3949ba59abbe56e057f20f883e")')
        return password


a = getPd()
logger.info(f'js生成的请求数据：{a}')
headers = headers = {'authority': 'passport.vip.com', 'method': 'POST', 'path': '/login/postLogin', 'scheme': 'https',
                     'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-encoding': 'gzip, deflate, br',
                     'accept-language': 'zh-CN,zh;q=0.9',
                     'authorization': a.get('headers'),
                     'cache-control': 'no-cache', 'content-length': '818',
                     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                     'cookie': f'vip_cps_cuid=CU1630332803537c9f24bd506e563c04; vip_cps_cid=1630332803540_55fee04c0eaf9160757bd613b8fcdbe3; cps_share=cps_share; vip_wh=VIP_NH; cps=adp%3Antq8exyc%3A%40_%401630332803539%3Amig_code%3A4f6b50bf15bfa39639d85f5f1e15b10f%3Aac014miuvl0000b5sq8cb1cokxut41di; PAPVisitorId=4081a8a00322453535c9569c10a511fa; vip_new_old_user=1; vip_address=%257B%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522cname%2522%253A%2522%255Cu73e0%255Cu6d77%255Cu5e02%2522%252C%2522pid%2522%253A%2522104104%2522%252C%2522cid%2522%253A%2522104104104%2522%257D; vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E7%8F%A0%E6%B5%B7%E5%B8%82; vip_city_code=104104104; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A0%7Cp4%3A0%7Cp5%3A0%7Cul%3A3105; mars_sid={a.get("sid")}; PHPSESSID=o4qlorb1vk3ocmo6gdse5ipfa3; mars_pid=0; visit_id=4BA3ECA41D66989858CD20237CA9535E; vip_tracker_source_from=; _jzqco=%7C%7C%7C%7C%7C1.1137832105.1630332817388.1630332817388.1630335720639.1630332817388.1630335720639.0.0.0.2.2; pg_session_no=4; mars_cid={a.get("cid")}',
                     'origin': 'https://passport.vip.com', 'pragma': 'no-cache',
                     'referer': 'https://passport.vip.com/login',
                     'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                     'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors',
                     'sec-fetch-site': 'same-origin',
                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                     'x-requested-with': 'XMLHttpRequest'}

data = {'api_key': '70f71280d5d547b2a7bb370a529aeea1', 'pc_eversion': '1', 'skey': '3c5ad16dbc06cd16ae1fd3344d87f16b',
        'pc_edata': a['pc_edata']}

r = requests.post(url, headers=headers, data=data)
logger.info(r.status_code)
logger.info(r.text)
