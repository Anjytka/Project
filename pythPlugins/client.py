# -*- coding: utf-8 -*-
import websocket
import json
from time import gmtime, strftime
from sys import stdin

f = None
dataAcc = []
dataGyr = []

def on_message(ws, message):
    global dataAcc, dataGyr, f
    if message == "whoIs":
        ws.send(json.dumps({"iAm": "recipient"}))
    else:
        if message == "Stop":
            lenAcc = len(dataAcc)
            lenGyr = len(dataGyr)
            print lenAcc, lenGyr
            if (lenAcc > lenGyr):
                dataAcc = dataAcc[:lenGyr]
            else:
                dataGyr = dataGyr[:lenAcc]

            print len(dataAcc), len(dataGyr)
            for i in range(dataGyr):
                f.write(dataAcc[i]+", "+dataGyr[i]+"\n")
        else:
            msg_data = json.loads(message)
            key = msg_data.keys()[0]
            if key == "acc": 
                dataAcc.append(str(msg_data[key]).strip('[]'))
            if key == "gyr":
                dataGyr.append(str(msg_data[key]).strip('[]'))

def on_error(ws, error):
    print "### Ошибка ###"
    print error

def on_close(ws):
    print "### Соединение закрыто ###"

def on_open(ws):
    global f
    print "### Соединение открыто ###"
    f.write("timeA,accx,accY,accZ,timeG,gyrX,gyrY,gyrZ\n")

    
if __name__ == "__main__":
    print "Введите имя папки для сохранения данных:"
    folderName = stdin.readline().strip()
    f = open(strftime(folderName+"/%Y-%m-%d %H:%M:%S.%s", gmtime())+'.csv', 'w')
    print "Введите ip-адрес и порт для соединения с сервером(в формате 0.0.0.0:0):"
    address = stdin.readline().strip()
    websocket.enableTrace(True)

    # ws = websocket.WebSocketApp("ws://178.62.197.146:3000/ws",
    ws = websocket.WebSocketApp("ws://"+address+"/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()