import sys
import numpy as np
import paho.mqtt.client as paho
import math
import time 


#callback function
def on_publish(client,userdata,result):             
    print(f"data published\n")
    pass
#push data to MQTT topic 
def push_to_server(broker, port, topic, comand, value):
    symbols = ['{', '"', '}']
    if comand == "forward":
        pusher = f"{symbols[0]}{symbols[1]}cmd{symbols[1]}: {symbols[1]}{str(comand)}{symbols[1]}, {symbols[1]}val{symbols[1]}: {symbols[1]}{str(value)}{symbols[1]}{symbols[2]}" #god forgive me for this...
    elif comand == "turn":
        angl = math.fabs(value)
        if value > 0:
            pusher = f"{symbols[0]}{symbols[1]}cmd{symbols[1]}: {symbols[1]}right{symbols[1]}, {symbols[1]}val{symbols[1]}: {symbols[1]}{str(angl)}{symbols[1]}{symbols[2]}"
        else: pusher = f"{symbols[0]}{symbols[1]}cmd{symbols[1]}: {symbols[1]}left{symbols[1]}, {symbols[1]}val{symbols[1]}: {symbols[1]}{str(angl)}{symbols[1]}{symbols[2]}"
    try:
        client1 = paho.Client("controller")                        
        client1.on_publish = on_publish                          
        client1.connect(broker, port)
        ret = client1.publish(topic, pusher) 
    except:
        print("Oops, starting data wasnt right or there is a problem on the server")
           
    

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

#function for calculating distance with: s_x, s_y == startingpoint cordinates; x,y == endpoint cordinates 
def distance(s_x, s_y, x, y):
    return math.sqrt((x - s_x) * (x - s_x) + (y - s_y) * (y - s_y))



#function for calculating angle with: s_x, s_y == startingpoint cordinates; x,y == endpoint cordinates.
#this function returns orientation "+" || "-" and the smallest angle; hours_wasted = 3.5
def turning_angle(s_x, s_y, x, y):

    angl = math.acos(((x * s_x + y * s_y) / (math.sqrt(x * x + y * y) * math.sqrt(s_x * s_x + s_y * s_y)))) * 180 / math.pi
    direction = math.degrees(math.atan2(x - s_x, y - s_y))
    if direction > 0:
        return -1 * angl
    else:
        return angl

#function for calculating time to move
def time_to_move(distance, velocity_ms):
    return math.fabs(distance / velocity_ms)

#function for calculating time to turn
def time_to_turn(angle, angle_velocity_degs):
    return math.fabs(angle / angle_velocity_degs)

#reads arguments and checks if they are all in place !!!!!!!!!!!!!NOT for dumb users!!!!!!!!!!!!!
def args_reading():
    args = sys.argv
    if len(args) != 6:
        print("improper data entered. \ndata changed to default values\n\n")
        return ["127.0.0.1", 1883, "/abot/command", 1.3, 20, "cord.txt"]
    else: return args





things = args_reading()
ip = things[0]#"127.0.0.1"
port = things[1]#1883
topic = things[2]#"abot/command"
velocity_ms = things[3]#1.3
angle_velocity_degs = things[4]#20
filename = things[5]#"cord.txt"
starting_angle = 0

v1_x = 0
v1_y = 0
v2_x = 0
v2_y = 5

cordinates = de_serialisaition(filename)
for i in range(1, len(cordinates)):
    
    xy_prev = cordinates[i - 1].split()

    xy = cordinates[i].split()
    

    x = float(xy[0])
    y = float(xy[1])
    pr_x = float(xy_prev[0])#previous cordinates
    pr_y = float(xy_prev[1])#previous cordinates
    v1_x = x - pr_x
    v1_y = y - pr_y

    _angle = turning_angle(float(v1_x), float(v1_y), float(v2_x), float(v2_y))

    print(f"turn {_angle}")
    push_to_server(ip, port, topic, "turn", _angle)
    time.sleep(time_to_turn(_angle, angle_velocity_degs))

    _distance = distance(float(x), float(y), float(pr_x), float(pr_y))

    print(f"move {_distance}")
    push_to_server(ip, port, topic, "forward", _distance)
    time.sleep(time_to_move(_distance, velocity_ms))

    angle = starting_angle
    v2_x = v1_x
    v2_y = v1_y




