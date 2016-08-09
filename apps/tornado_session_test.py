import os
import sys

# sys.path.append("~/Desktop/codes/sentimeter-backend/")
sys.path.append("~/var/www/ginsoy/sentimeter-backend/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lively.settings")
from apps.redis_queue import RedisQueue
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import time
from tornado.options import options, define, parse_command_line
class SampleWebSocket(WebSocketHandler):
    clients = []
    userid = 1

    print("yes came in",)
    print(len(clients))
    def check_origin(self, origin):
        return True
    def open(self):
        length = 0
        q = RedisQueue('feedback_redis_queue')
        self.clients.append(self)
        print("connection_initiated")
        print(self.clients)
        print(len(self.clients))
        abc = q.seek()
        print("1",q)
        print("2",abc)
        print("3",abc[0])
        data = abc[0].decode("utf-8")
        print(str(data))
        while True:
            if length < q.qsize():
                length = q.qsize()
                print("true")
                print(self.clients)
                print(len(self.clients))


                self.write_message("%s" % str(data))
                time.sleep(10)
    def on_close(self):
        self.clients.remove(self)
        self.write_message("connection_closed")

app = Application([
    (r'/live/', SampleWebSocket),
    ],)

if __name__ == '__main__':
    http_server = HTTPServer(app)
    print("b")
    # http_server.bind(8888)
    http_server.bind(5678)
    http_server.start(0)
    print("starting")
    IOLoop.current().start()