#help link "https://github.com/aaugustin/websockets"
__author__ = 'aamish'

import asyncio
import websockets
from apps.redis_queue import RedisQueue
import random
from lively import settings


@asyncio.coroutine
def ping(websocket, path):
    q = RedisQueue('feedback_redis_ginsoy')
    print("Connection Opened")
    length = 0
    while True:
        if websocket.open:
            if length < q.qsize():
                length = q.qsize()
                abc = q.seek()
                data = abc[0].decode("utf-8")
                print("Ping Received")
                yield from websocket.send(str(data))
                yield from asyncio.sleep(random.random() * 3)
        else:
            return

start_server = websockets.serve(ping, settings.WEBSOCKET_ADDRESS, settings.WEBSOCKET_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()