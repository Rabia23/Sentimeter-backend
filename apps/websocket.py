#help link "https://github.com/aaugustin/websockets"
__author__ = 'aamish'

import asyncio
import websockets
from apps.redis_queue import RedisQueue
import random
from lively import settings


@asyncio.coroutine
def ping(websocket, path):
    q1 = RedisQueue('feedback_redis_mc_qatar')
    q2 = RedisQueue('feedback_redis_ginsoy')
    print("Connection Opened")
    length = 0
    while True:
        if websocket.open:
            if length < q1.qsize():
                print("in feed back qatar")
                length = q1.qsize()
                abc1 = q1.seek()
                data1 = abc1[0].decode("utf-8")
                print("Ping Received")
                yield from websocket.send(str(data1))
                yield from asyncio.sleep(random.random() * 3)

            if length < q2.qsize():
                print("in feed back ginsoy")
                length = q2.qsize()
                abc2 = q2.seek()
                data2 = abc2[0].decode("utf-8")
                print("Ping Received")
                yield from websocket.send(str(data2))
                yield from asyncio.sleep(random.random() * 3)
        else:
            return

start_server = websockets.serve(ping, settings.WEBSOCKET_ADDRESS, settings.WEBSOCKET_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()