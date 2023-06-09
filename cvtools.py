import cv2
import numpy as np

kernel = np.ones((5, 5), np.uint8)

def GetColorMask(img: cv2.Mat, boundaries):
    img = cv2.medianBlur(img, 3)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    im = cv2.inRange(hsv, boundaries[0][0], boundaries[0][1])
    for i in range(1, len(boundaries)):
        im += cv2.inRange(hsv, boundaries[i][0], boundaries[i][1])
    return im

def ClearMask(img):
    #processed = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    #cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
    return cv2.dilate(img, kernel)
    
def FindObject(img: cv2.Mat, area, boundaries):
    processed = ClearMask(GetColorMask(img, boundaries))
    contours, _ = cv2.findContours(
        processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) > area:
            return cv2.boundingRect(contour) + (True,)
    return (-1, -1, -1, -1, False)