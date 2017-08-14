#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json
from sys import stdin

class WSHandler(tornado.websocket.WebSocketHandler):
    recipient = None
    sender = None

    def open(self):
        print "Новое соедиение"
        self.write_message("whoIs")


    def on_message(self, message):
        msg = json.loads(message)
        print msg
        key = msg.keys()[0]
        if (key == "iAm"):
            if (msg["iAm"] == "sender") and \
               (WSHandler.sender is None):
                    WSHandler.sender = self
                    print "Подключение с мобильным устройством установлено"
            if (msg["iAm"] == "recipient") and \
               (WSHandler.recipient is None):
                    WSHandler.recipient = self
                    print "Подключение с модулем на компьютере установлено"
        else:
            if (key in ["acc", "gyr"]) and not(WSHandler.recipient is None):
                WSHandler.recipient\
                    .write_message(json.dumps(msg))


    def on_close(self):
        if WSHandler.sender == self:
            WSHandler.sender = None
            print "Соединение с модулем на компьютере потеряно"
            if not(WSHandler.recipient is None):
                WSHandler.recipient.write_message("Stop")
        if WSHandler.recipient == self:
            WSHandler.recipient = None
            print "Соединение с мобильным устройством потеряно"
        


application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
    print "Сервер готов к работе"
    print "Введите порт для обмена данными (от 1024-65535):"
    address = stdin.readline().strip()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3000)
    tornado.ioloop.IOLoop.instance().start()



    