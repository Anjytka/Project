import websocket
import time
import json
import datetime

f = None

def on_message(ws, message):
    if message == 'whoIs':
        response = {'iAm': "recipient"}
        ws.send(json.dumps({'iAm': 'recipient'}))
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
    time = datetime.datetime.now()
    f = open(strftime("%Y-%m-%d_%H-%M-%S", time)+'.csv', 'w')
    f.write("timeA,accx,accY,accZ,timeG,gyrX,gyrY,gyrZ\n")

    
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://178.62.197.146:3000/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()