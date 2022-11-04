import os
import paho.mqtt.client as mqtt 
import time

#this function reads a file of hist with defined name
def de_serialisaition(name):
    hist = []
    try:
      f = open(name, 'r')
    except: 
        print("file not found") 
        _hist = [0]
        return _hist
    for line in f:
        hist.append(line)
    f.close()
    return hist

def Update_File():
    h1 = str(de_serialisaition('user.txt'))
    os.system(f'.\mos2\mosquitto_pub -t test/test -m "' + str(h1) + '"')
    print("file posted")



#mqttBroker ="mqtt.eclipseprojects.io" 
#   client = mqtt.Client("trasmitter")


#client.connect(mqttBroker)
while 1 == 1:
    Update_File()

    #client.publish("histogram/h", str(de_serialisaition('user.txt')))
    #client.publish("histogram/h", "1234567")
    time.sleep(5)
   