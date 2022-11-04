import os
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



while 1 == 1:
    Update_File()
    
    time.sleep(5)
   
