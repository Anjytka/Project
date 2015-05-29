#!/usr/bin/python

import datetime
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json

class WSHandler(tornado.websocket.WebSocketHandler):
    recipient = None
    sender = None
    user_type = None

    def open(self):
        print 'New connection'
        self.write_message("whoIs")


    def on_message(self, message):
        msg = json.loads(message)
        # print "The connecting client length is: %s" % len(WSHandler.clients)
        # print "The connecting user type is: %s" % WSHandler.user_type
        if (WSHandler.sender is None) or (WSHandler.recipient is None):
            WSHandler.user_type = msg['iAm']
            if WSHandler.user_type == 'recipient':
                WSHandler.recipient = self
                #self.write_message(msg)
                print "The connecting client is: %s" % WSHandler.user_type

            if WSHandler.user_type == 'sender':
                # self.write_message(msg)
                WSHandler.sender = self
                print "The connecting client is: %s" % WSHandler.user_type
        else:
            msg_data = msg['sCh']
            WSHandler.recipient.write_message(json.dumps(msg_data))
            # for con in WSHandler.clients:
                # con.write_message(json.dumps(msg_type))
#            self.write_message(json.dumps(msg_type))
#            print str(msg_type).strip('[]')


    def on_close(self):
        if WSHandler.sender == self:
            WSHandler.sender = None
        if WSHandler.recipient == self:
            WSHandler.recipient = None
        print 'Connection closed'
        


application = tornado.web.Application([
  (r'/ws', WSHandler),
])
#websocket writing 5:::{"name":"sCh","args":[1414269113222,-1.8413162,5.1193733,18.711994,-136.91325,-5.285813,-4.089551]}

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3000)
    tornado.ioloop.IOLoop.instance().start()



    