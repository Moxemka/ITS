import paho.mqtt.client as mqtt
import math
import json
import pygame
from threading import Thread
import pygame
###hours spent ~10.5

class Bot():
    def __init__(self, x, y, alpha, moving_speed, turning_speed):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.ms = moving_speed
        self.ts = turning_speed

    #counting distance    
    def count_distance(self, moving_speed, time):
        return moving_speed * time

    #counting degree
    def count_alpha(self, turning_speed, time):
        return turning_speed * time

    #counting new x position
    def new_x(self, alpha, moving_speed, time):
        return math.cos(math.radians(alpha)) * self.count_distance(moving_speed, time)

    #counting new y position
    def new_y(self, alpha, moving_speed, time):
        return math.sin(math.radians(alpha)) * self.count_distance(moving_speed, time)
   
    #changing internal x and y position as we moved forward
    def go_forward(self, value):
        if 0 <= self.alpha <= 90:
            self.x += self.new_x(self.alpha, self.ms, value) 
            self.y += self.new_y(self.alpha, self.ms, value)
        elif 90 < self.alpha <= 180:
            self.x -= self.new_x(self.alpha, self.ms, value) 
            self.y += self.new_y(self.alpha, self.ms, value)
        elif 180 < self.alpha <= 270:
            self.x -= self.new_x(self.alpha, self.ms, value) 
            self.y -= self.new_y(self.alpha, self.ms, value)
        elif 270 < self.alpha <= 359:
            self.x += self.new_x(self.alpha, self.ms, value) 
            self.y -= self.new_y(self.alpha, self.ms, value)
        print("bot move forward " + str(value) + "s")

    #changing internal x and y position as we moved backwards
    def go_backwards(self, value):
        if 0 <= self.alpha <= 90:
            self.x -= self.new_x(self.alpha, self.ms, value) 
            self.y -= self.new_y(self.alpha, self.ms, value)
        elif 90 < self.alpha <= 180:
            self.x += self.new_x(self.alpha, self.ms, value) 
            self.y -= self.new_y(self.alpha, self.ms, value)
        elif 180 < self.alpha <= 270:
            self.x += self.new_x(self.alpha, self.ms, value) 
            self.y += self.new_y(self.alpha, self.ms, value)
        elif 270 < self.alpha <= 359:
            self.x -= self.new_x(self.alpha, self.ms, value) 
            self.y += self.new_y(self.alpha, self.ms, value)
        print("bot move backwards " + str(value) + "s")
    #checking if angle stays positive and contained in [0, 359]
    def check_overflow(self):
        if self.alpha >= 360: self.alpha -= 360
        elif self.alpha <= -360: self.alpha += 360
        self.alpha = math.fabs(self.alpha)
    #changing internal alpha angle global position as we turning left
    def turn_left(self, value):
        self.alpha += self.count_alpha(self.ts, value)
        self.check_overflow()
        print("bot turn left " + str(value) + "s")
        
    #changing internal alpha angle global position as we turning right
    def turn_right(self, value):
        self.alpha -= self.count_alpha(self.ts, value)
        self.check_overflow()    
        print("bot turn right " + str(value) + "s")

    #stopping bot... commands no more!
    def stop(self):
        print("bot stop")



bot = Bot(0, 0, 90, 0.3, 10) #creating global instance of bot



#handling bot commands and telling them to a bot
def Bot_Command(command, val):
    print(f"value taken: {val}")
    value = float(val)


    if command == "forward":

        bot.go_forward(value)
        print(f"new x: {bot.x}; new y: {bot.y}; move {bot.count_distance(bot.ms, value)}")#can be deleted, they are for debbuging purposes

    elif command == "backwards": 

        bot.go_backwards(value)
        print(f"new x: {bot.x}; new y: {bot.y}; move {bot.count_distance(bot.ms, value)}")#can be deleted, they are for debbuging purposes

    elif command == "left":

        bot.turn_left(value)
        print(f"turn {bot.count_alpha(bot.ts, value)} new global degree: {bot.alpha};")#can be deleted, they are for debbuging purposes

    elif command == "right":

        bot.turn_right(value)
        print(f"turn {bot.count_alpha(bot.ts, value)} new global degree: {bot.alpha};")#can be deleted, they are for debbuging purposes

    elif command == "stop":
        bot.stop()


broker = '127.0.0.1'
port = 1883
topic = "/abot/command"
client_id = 'Bot'


#connecting and checking if we able to connect
def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else: 
            print("Failed to connect, return code %d\n", rc)
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive = 200)
    return client

#subscribing to a topic
def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        message = json.loads(msg.payload.decode())
        try:
            if "val" in message.keys():#checking for contained command and value 
                Bot_Command(message["cmd"], round(float(message["val"]), 1))
            else:
                Bot_Command(message["cmd"], 0)
        except:
            print(f"Received command {msg.payload.decode()} cant be decoded")
        
    client.subscribe(topic)
    client.on_message = on_message

#thread for drawing
def draw_thread():
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))
    screen = pygame.display.set_mode((720, 480))
    clock = pygame.time.Clock()
    FPS = 60 # Frames per second.
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255) # RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).
    rect = pygame.Rect((0, 0), (32, 32))
    image = pygame.Surface((32, 32))
    image.fill(WHITE) 
    while True:
        rect.x = bot.x
        rect.y = bot.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        screen.fill(BLACK)
        screen.blit(image, rect)
        pygame.display.update() 


#running client
def run():
    my_thread = Thread(target=draw_thread)
    my_thread.start()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
   

if __name__ == '__main__':
    run()




