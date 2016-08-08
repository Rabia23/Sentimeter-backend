# -*- coding: utf-8 -*-

"""
Regular expression groups in URL pattern are passed as arguments to "open"
method of tornado.websocket.WebSocketHandler
"""
import os
import sys

# Setup Django environment so that we can access Django models
sys.path.append("~/Desktop/codes/sentimeter-backend/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lively.settings")
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import time

class SampleWebSocket(WebSocketHandler):
    clients = []
    print("yes came in")
    print(len(clients))
    def check_origin(self, origin):
        return True
    def open(self, userid):
        self.clients.append(self)
        print("connection_initiated")
        print(self.clients)
        print(len(self.clients))
        # while True:
        #     print("true")
        #     print(self.clients)
        #     print(len(self.clients))
        #
        #     time.sleep(5)
        self.write_message("%s" % userid)
    def on_close(self):
        self.clients.remove(self)
        self.write_message("connection_closed")

app = Application([
    (r'/ws/(.*)', SampleWebSocket),
    ],)

if __name__ == '__main__':
    http_server = HTTPServer(app)
    print("b")
    http_server.bind(8888)
    http_server.start(0)
    print("starting")
    IOLoop.current().start()