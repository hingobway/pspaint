import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)


def die(*arg):
    pass


cv.namedWindow('settings')
cv.createTrackbar('lhue', 'settings', 95, 255, die)
cv.createTrackbar('lsat', 'settings', 197, 255, die)
cv.createTrackbar('lval', 'settings', 0, 255, die)
cv.createTrackbar('hhue', 'settings', 102, 255, die)
cv.createTrackbar('hsat', 'settings', 255, 255, die)
cv.createTrackbar('hval', 'settings', 253, 255, die)

points = []
draw = False

while(True):
    _, img = cap.read()

    img = cv.flip(img, 1)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #  Make mask
    lhue = cv.getTrackbarPos('lhue', 'settings')
    lsat = cv.getTrackbarPos('lsat', 'settings')
    lval = cv.getTrackbarPos('lval', 'settings')
    hhue = cv.getTrackbarPos('hhue', 'settings')
    hsat = cv.getTrackbarPos('hsat', 'settings')
    hval = cv.getTrackbarPos('hval', 'settings')
    out = cv.inRange(hsv, np.array(
        [lhue, lsat, lval]), np.array([hhue, hsat, hval]))

    M = cv.moments(out)

    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if draw:
            points.append((cX, cY))

    for i in range(1, len(points)):
        if(type(points[i]) == tuple and type(points[i-1]) == tuple):
            cv.line(img, points[i], points[i-1], (255, 255, 255), 4)

    cv.imshow('img', img)

    val = cv.waitKey(1)

    if(val == ord('m')):
        points = []
    if(val == ord(' ')):
        draw = not draw
        points.append(None)

    if(val == ord('q')):
        break
