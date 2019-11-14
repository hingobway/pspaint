import cv2 as cv
import numpy as numpy

cap = cv.VideoCapture(0)

while(True):
    _, img = cap.read()

    img = cv.flip(img, 1)

    cv.imshow('track', img)

    if(cv.waitKey(1) == ord('q')):
        break
