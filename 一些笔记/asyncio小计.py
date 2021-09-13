'''
pip install aiohttp,aiofiles
pip install aiodns
'''

''''
切记，异步代码不能与同步代码混用，否则如果同步代码耗时过长，异步代码就会被阻塞，失去异步的效果。
而网络请求和文件操作是整个流程中最耗时的部分，所以我们必须使用异步的库来进行操作！否则就白搞了
'''
import aiohttp
import aiofiles
import asyncio

'''异步请求'''
# aiohttp和asyncio都不能识别time.sleep(),文件读取等耗时操作，
# 如果认为中出现不支持异步的耗时操作，那么这些耗时操作会以同步的方式执行
'''pip install aiohttp'''


headers = {}
params = {}
proxies = "http://proxy.com"


# 发起请求和获取响应都是io操作，用await修饰来切换任务
async def get_text(url,semaphore):  # 定义协程函数，即定义任务
    async with semaphore:   # 限制最大并发数
        # trust_env = True    获取本地代理
        async with aiohttp.ClientSession(trust_env=True) as sess:  # 创建连接对象
            # 发起请求
            # sess对象请求与requests基本相同
            # async with await sess.request()
            # async with await sess.post(url=url, headers=headers, data=data, proxy=proxies) as r:
            # 默认情况下，aiohttp对HTTPS协议使用严格的检查。通过将ssl设置为False
            async with sess.get(url=url, headers=headers, params=params, proxy=proxies,ssl =False ) as r:
                r.status  # 响应状态码
                # r.encoding # 编码
                r.history
                r.headers
                r.request_info.headers
                r1 = await r.text()  # 字符形式的响应
                # await r.text(encoding='utf-8')   # 自己知道编码·
                # r1=await r.read()      # 字节形式的响应
                # r1=await r.json()      # json形式的响应
                # r.content.read(100)    # 流式下载，不会全部加加载到内存


url_list = []


async def main():
    semaphore = asyncio.Semaphore(3)  # 限制最大并发数为3
    tasks = [asyncio.create_task(get_text(i,semaphore)) for i in url_list]
    asd = [await i for i in asyncio.as_completed(tasks)]
    return asd


loop = asyncio.get_event_loop()
result = loop.run_until_complete(main())  # result 是main函数的返回结果

'''
要将自己的cookie发送到服务器，可以使用构造函数的cookies 参数ClientSession：
url = 'http://httpbin.org/cookies'
cookies = {'cookies_are': 'working'}
async with ClientSession(cookies=cookies) as session:
'''

'''
大文件下载
with open(filename, 'wb') as fd:
    while True:
        chunk = await resp.content.read(chunk_size)
        if not chunk:
            break
        fd.write(chunk)
'''

'''返回这种结果时要将http变为https，verify=False'''
'''
<html>
<head>
<script language="javascript">setTimeout("location.replace(location.href.split(\"#\")[0])",1000);</script>
</head>
<iframe src="http://10.182.100.200:89/flashredir.html" frameborder=0></iframe>
</html>
'''

'''异步读取文件'''


async def wirte_demo():
    # 异步方式执行with操作,修改为 async with
    async with aiofiles.open("text.txt", "w", encoding="utf-8") as fp:
        await fp.write("hello world ")
        print("数据写入成功")


async def read_demo():
    async with aiofiles.open("text.txt", "r", encoding="utf-8") as fp:
        content = await fp.read()
        print(content)


async def read2_demo():
    async with aiofiles.open("text.txt", "r", encoding="utf-8") as fp:
        # 读取每行
        async for line in fp:
            print(line)


if __name__ == "__main__":
    asyncio.run(wirte_demo())
    asyncio.run(read_demo())
    asyncio.run(read2_demo())
