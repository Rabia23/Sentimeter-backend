#help link "https://github.com/aaugustin/websockets"
__author__ = 'aamish'

import asyncio
import websockets
from apps.redis_queue import RedisQueue
import random
from lively import settings


@asyncio.coroutine
def ping(websocket, path):
    q_qatar = RedisQueue('feedback_redis_mc_qatar')
    q_jinsoy = RedisQueue('feedback_redis_ginsoy')
    print("Connection Opened")
    length = 0
    while True:
        if websocket.open:
            if length < q_qatar.qsize():
                length = q_qatar.qsize()
                abc_qatar = q_qatar.seek()
                data_qatar = abc_qatar[0].decode("utf-8")
                print("Ping Received")
                print("in feed back qatar")
                yield from websocket.send(str(data_qatar))
                yield from asyncio.sleep(random.random() * 3)
            if length < q_jinsoy.qsize():
                length = q_jinsoy.qsize()
                abc_jinsoy = q_jinsoy.seek()
                data_jinsoy = abc_jinsoy[0].decode("utf-8")
                print("Ping Received")
                print("in feed back qatar")
                yield from websocket.send(str(data_jinsoy))
                yield from asyncio.sleep(random.random() * 3)
        else:
            return

start_server = websockets.serve(ping, settings.WEBSOCKET_ADDRESS, settings.WEBSOCKET_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()