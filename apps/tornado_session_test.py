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
class SampleWebSocket(WebSocketHandler):
    check_len = 0
    clients = []
    print("yes came in1",)
    def check_origin(self, origin):
        return True


    def open(self):

        q = RedisQueue('feedback_redis_queue')
        self.clients.append(self)
        print("connection_initiated1")
        print("1q size",q.qsize())
        length = self.check_len
        print("len",length)
        abc = q.seek()
        print("selfchec01", self.check_len)
        # print("1",q)
        # print("2",abc)
        # print("3",abc[0])
        data = abc[0].decode("utf-8")
        # print(str(data))
        while True:
            if length < q.qsize():
                length = q.qsize()
                self.check_len = length
                print("selfchec11",self.check_len)
                # length = q.qsize()
                print("true1")
                self.write_message("%s" % str(data))
                # time.sleep(10)
    def on_close(self):
        self.clients.remove(self)
        print("closing1")
        self.write_message("connection_closed")
class SampleWebSocketQatar(WebSocketHandler):
    clients_qatar = []
    check_len_qatar = 0
    print("2yes came in qatar",)
    def check_origin(self, origin):
        return True


    def open(self):

        q_qatar = RedisQueue('feedback_redis_mc_qatar')
        self.clients_qatar.append(self)
        print("2connection_initiated")
        print("2q _qatar size",q_qatar.qsize())
        length_qatar = self.check_len_qatar
        print("len_qatar",length_qatar)
        abc_qatar = q_qatar.seek()
        print("selfchec22_qatar", self.check_len_qatar)
        # print("1",q)
        # print("2",abc)
        # print("3",abc[0])
        data_qatar = abc_qatar[0].decode("utf-8")
        # print(str(data))
        while True:
            if length_qatar < q_qatar.qsize():
                length_qatar = q_qatar.qsize()
                self.check_len_qatar = length_qatar
                print("selfchec22_qatar",self.check_len_qatar)
                # length = q.qsize()
                print("true2_qatar")
                self.write_message("%s" % str(data_qatar))
                # time.sleep(10)
    def on_close(self):
        self.clients_qatar.remove(self)
        print("closing2_qatar")
        self.write_message("connection_closed2")
app = Application([
    (r'/live/', SampleWebSocket),
    (r'/test1/', SampleWebSocketQatar),
    ], )

if __name__ == '__main__':
    http_server = HTTPServer(app)
    # http_server.bind(8888)
    http_server.bind(5678)
    http_server.start(0)
    # IOLoop.instance().start()
    IOLoop.current().start()