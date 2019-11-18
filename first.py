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
color=(255,255,255)

circles=[(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
radius=45
pad=15

while(True):
    _, img = cap.read()
    height,width=img.shape[:2]

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

    # Find Center
    M = cv.moments(out)

    cursor=None
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if draw:
            points.append((cX, cY))
        else:
            cursor=(cX,cY)

    # Plot drawings
    for i in range(1, len(points)):
        if(type(points[i]) == tuple and type(points[i-1]) == tuple):
            cv.line(img, points[i], points[i-1], color, 4)

    # Plot Circles
    if not draw:
        

        for i in range(0,len(circles)):
            x=round(radius+pad)
            y=round((((height/len(circles))*i) + ((height/len(circles))/2)))
            cv.circle(img, (x,y),radius,circles[i],-1)

            if(cursor):
                d=np.sqrt(((cursor[0]-x)**2)+((cursor[1]-y)**2))
                if(d<=radius):
                    color=circles[i]

    if(cursor):
        # Plots cursor when not drawing, makes the color black if over a circle.

        curColor=color
        for i in range(0,len(circles)):
            x=round(radius+pad)
            y=round((((height/len(circles))*i) + ((height/len(circles))/2)))

            if(cursor):
                d=np.sqrt(((cursor[0]-x)**2)+((cursor[1]-y)**2))
                if(d<=radius):
                    curColor=(0,0,0)

        cv.circle(img,cursor,5,curColor,-1)
        


    cv.imshow('img', img)


    # UX
    val = cv.waitKey(1)

    if(val == ord('m')):
        points = []
    if(val == ord(' ')):
        draw = not draw
        points.append(None)

    if(val == ord('q')):
        break
