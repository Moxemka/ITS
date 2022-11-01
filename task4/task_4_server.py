import os

#this function creates a file of hist with defined name
def serialisaition(hist1, name):
      f = open(name + '.txt', 'w')
      for i in range(0, len(hist1)):
          f.write(str(hist1[i]) + '\n')
      f.close()
      print('file created with name = ',name,'.txt')

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

def Start_Server():
    os.system('.\mos2\mosquitto -v')

def Sub_To():
    os.system('.\mos2\mosquitto_sub -t test/test')

def Update_File():
    h1 = str(de_serialisaition('user.txt'))
    print('.\mos2\mosquitto_pub -t ''test/topic'' -m ')
    os.system(f'.\mos2\mosquitto_pub -t test/test -m "' + str(h1) + '"')


#Start_Server()
#Update_File()
while 1 == 1:
    input()
    Update_File()