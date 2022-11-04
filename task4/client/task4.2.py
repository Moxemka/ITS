import os
import sys
import paho.mqtt.client as mqtt
import time
import re

def moving_average(v):
    sum = 0.0
    for t in range(2, len(v) - 1):
        sum += float(v[t])*0.6+float(v[t-1])*0.3+float(v[t-2])*0.1
    return sum

def Convert(string):
    li = []
    try:
        li = re.findall(r"\d+", string)
        print("converted: " + str(li))
        return li
    except: print("error")


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("test/test")

def on_message(client, userdata, msg):
    print('moving average ' + str(moving_average(Convert(msg.payload.decode()))))
    client.disconnect()

while 1 == 1:  
    os.system('cls')
    client = mqtt.Client()
    client.connect("127.0.0.1", 1883)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
    
    





