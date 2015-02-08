import websocket
import thread
import time
import json


def on_message(ws, message):
    if message == 'whoIs':
        response = {'iAm': "reader"}
        ws.send(json.dumps({'iAm': 'reader'}))
    else:
        msg_data = json.loads(message)
        print str(msg_data).strip('[]')

def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### open ###"
    
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:3000/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()