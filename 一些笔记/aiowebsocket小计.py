''' 测试地址：ws://echo.websocket.org/'''


'''https://www.bitforex.com/en/spot/btc_usdt'''
import asyncio
import logging
from datetime import datetime
from aiowebsocket.converses import AioWebSocket
import json
import  time

'''请求开始是上传的数据'''
message1 =[{"type":"subHq_cancel_all","event":"kline"}]
message2 =[{"type":"subHq","event":"kline","param":{"businessType":"coin-usdt-btc","kType":"30min","size":1440}}]
async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator
        # 客户端给服务端发送消息
        await converse.send(json.dumps(message1))
        await converse.send(json.dumps(message2))
        while True:
            # t = time.time()
            # if int(t)%10==0:
            #     await converse.send('ping_p')
            mes = await converse.receive()
            # print('{time}-Client receive: {rec}'
            #       .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=mes.decode()))
            # with open('1.json','wb') as f:
            #     f.write(mes)
            print(mes)


if __name__ == '__main__':
    remote = 'wss://www.bitforex.com/mkapi/coinGroup1/ws'
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
    except KeyboardInterrupt as exc:
        logging.info('Quit.')
