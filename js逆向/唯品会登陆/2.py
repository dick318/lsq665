import requests

headers = {
    'authority': 'mapi.vip.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://list.vip.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
}

params = (
    ('callback', 'getMerchandiseDroplets1'),
    ('app_name', 'shop_pc'),
    ('app_version', '4.0'),
    ('warehouse', 'VIP_SH'),
    ('fdc_area_id', '103103105'),
    ('client', 'pc'),
    ('mobile_platform', '1'),
    ('province_id', '103103'),
    ('api_key', '70f71280d5d547b2a7bb370a529aeea1'),
    ('user_id', ''),
    ('mars_cid', '1630378403147_34d7824bc7737a0cea1d0c7d100741ae'),
    ('wap_consumer', 'a'),
    ('productIds', '6919447779396977232,6919460809797396995,6919423157581011397,6919208534751337501,6919330241334072392,6919032831667362824,6919224409114131528,6919431462440934403,6919315838469424072,6919447782329886021,6919218867516611656,6919267955334854789,6919462297610350664,6919307117984709128,6919370941576918533,6919226105360783813,6919238028844902789,6919025976441658376,6919182186056021125,6919421751649825864,6919286819228635976,6919154900968854920,6919266438820673669,6919143410396674760,6919062154877805960,6919240917830871688,6919396946915097157,6919220367438298184,6919285507568456520,6919457977735014533,6919421751683576904,6919420059193839811,6919409973729463112,6919453461256952323,6919398163984694275,6919467767565698181,6919408551405388803,6919471099530745349,6919396946898250309,6919463866903831685,6919399962853747075,6919281175091163976,6919112577147691461,6918808281363679813,6919431879398566915,6919341591178649928,6919453461257001475,6919421751480906824,6919236060788688456,6919124369813128456'),
    ('scene', 'rule_stream'),
    ('standby_id', 'nature'),
    ('extParams', '{"stdSizeVids":"","preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x","ic2label":1}'),
    ('context', ''),
    ('_', '1630937689016'),
)

response = requests.get('https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2', headers=headers, params=params)

print(response.status_code)
print(response.text)