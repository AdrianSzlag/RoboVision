import numpy as np
import cv2
import time
import fastweb as web
from camera import CameraFeed
from controller import SerialControler, Directions
from cvtools import FindObject

REMOTE_CONTROLL = 1
AUTOMATIC_CONTROLL = 2

arduino = SerialControler().start()

colorBoundaries = [(np.array([0 / 2, 0.4*255, 0.3*255]), np.array([20 / 2, 1*255, 1*255])),
                   (np.array([340 / 2, 0.4*255, 0.35*255]), np.array([360 / 2, 1*255, 1*255]))]

textColor = (0, 0, 0)
font = cv2.FONT_HERSHEY_SIMPLEX
targetWidth = 0.4
tolx = 0.1
toly = 0.1
minArea = 200
controll = REMOTE_CONTROLL

def sendDirections(item, controllType):
    if controll == controllType:
        arduino.write(item)

def update(img: cv2.Mat):
    x, y, w, h, grabbed = FindObject(img, minArea, colorBoundaries)
    if grabbed == True:
        distance = (w/img.shape[1]) / targetWidth
        center = ((x + w/2) / img.shape[1]) - 0.5
        item = Directions()
        if distance > 1 + toly:
            item.backward = True
        if distance < 1 - toly:
            item.forward = True
        if center < -tolx:
            item.left = True
        if center > tolx:
            item.right = True
        sendDirections(item, AUTOMATIC_CONTROLL)
        if item.isStatic() == False:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
        else:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
        cv2.putText(img, str(w/img.shape[1]),
                    (int(img.shape[0]*0.4), int(img.shape[0]*0.9)), font, 1, (0, 255, 0))
        # cv2.putText(img, str((x+(w/2) - img.shape[1]/2)/img.shape[1]), (int(
        #   img.shape[0]*0.4), int(img.shape[0]*0.8)), font, 1, (0, 255, 0))

    cv2.putText(img, 'Fps camera ' + str(cam.getFps()),
                (10, 30), font, 1, textColor)
    cv2.putText(img, 'Fps web ' + str(web.getFps()),
                (10, 60), font, 1, textColor)        
    web.pushFrame(img)

def webChangeControll(item: web.Controll):
    global controll
    if item.controll == "REMOTE_CONTROLL":
        controll = REMOTE_CONTROLL
        return item
    if item.controll == "AUTOMATIC_CONTROLL":
        controll = AUTOMATIC_CONTROLL
        return item
    item.controll = controll
    return item

web.init(lambda item : sendDirections(item, REMOTE_CONTROLL), webChangeControll)
web.start()
cam = CameraFeed(update).start()

while True:
    time.sleep(1)
