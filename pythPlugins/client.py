import websocket
import thread
import time
import json

f = open("text.txt", 'w')

def on_message(ws, message):
    if message == 'whoIs':
        response = {'iAm': "reader"}
        ws.send(json.dumps({'iAm': 'reader'}))
    else:
        msg_data = json.loads(message)
        data = str(msg_data).strip('[]')
        print data
        f.write(data+"\n")

def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### open ###"
    
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://178.62.197.146:3000/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()