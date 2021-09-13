'''https://mp.weixin.qq.com/s/WoYQfEbmTAxibvtitUQLzg'''
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
import random

ORIGIN_CIPHERS = ('ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
                  'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES')


class DESAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        """
        A TransportAdapter that re-enables 3DES support in Requests.
        """
        CIPHERS = ORIGIN_CIPHERS.split(':')
        random.shuffle(CIPHERS)
        CIPHERS = ':'.join(CIPHERS)
        self.CIPHERS = CIPHERS + ':!aNULL:!eNULL:!MD5'
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'}
s = requests.Session()
s.headers.update(headers)

for _ in range(5):
    s.mount('https://ja3er.com', DESAdapter())
    resp = s.get('https://ja3er.com/json').json()
    print(resp)












'''aiohttp'''
# import random
# import ssl
# import asyncio
# import aiohttp
#
# # ssl._create_default_https_context = ssl._create_unverified_context
#
#
# ORIGIN_CIPHERS = ('ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
#                   'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES')
#
#
# class SSLFactory:
#     def __init__(self):
#         self.ciphers = ORIGIN_CIPHERS.split(":")
#
#     def __call__(self) -> ssl.SSLContext:
#         random.shuffle(self.ciphers)
#         ciphers = ":".join(self.ciphers)
#         ciphers = ciphers + ":!aNULL:!eNULL:!MD5"
#
#         context = ssl.create_default_context()
#         context.set_ciphers(ciphers)
#         return context
#
#
# sslgen = SSLFactory()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         for _ in range(5):
#             async with session.get("https://ja3er.com/json", headers={}, ssl=sslgen()) as resp:
#                 data = await resp.json()
#                 print(data)
#
# asyncio.get_event_loop().run_until_complete(main())