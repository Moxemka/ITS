import numpy as np
import cv2 #docker: pip install opencv-python-headless
import paho.mqtt.client as paho



def event_l_button(event,x,y,flags,params):
    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        rect_x.append(x)
        rect_y.append(y)
        push_to_server();




def on_publish(client,userdata,result):             
    print("data published \n")
    pass
def push_to_server():
    broker="127.0.0.1"
    port=1883
    client1 = paho.Client("controller")                          
    client1.on_publish = on_publish                          
    client1.connect(broker,port)
    rect_xy = ' x ' + str(rect_x) + ' y ' + str(rect_x)
    print(f'data published = {rect_xy}')
    ret= client1.publish('position', str(rect_xy))


video_path = input()

capture = cv2.VideoCapture('video.mp4')


cv2.namedWindow(winname='video')
cv2.setMouseCallback('video', event_l_button)
rect_x = []
rect_y = []


while(capture.isOpened()):
    ret, frame = capture.read()

    #operations on frame
    
    for i in range(0, len(rect_x)):
        cv2.rectangle(frame, (rect_x[i] - 30, rect_y[i] - 30),(rect_x[i] + 30, rect_y[i] + 30), (0, 0, 255), 5)


    if cv2.waitKey(1) & 0xFF == ord('c'): 
        rect_x = []
        rect_y = []    

    #dispaying results
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    
    


capture.release()
cv2.destroyAllWindows()