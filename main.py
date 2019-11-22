import cv2 as cv
import numpy as np

import circles

cap = cv.VideoCapture(0)


def die(*arg):
    pass


# cv.namedWindow('settings')
# cv.createTrackbar('lhue', 'settings', 95,  255, die)
# cv.createTrackbar('lsat', 'settings', 197, 255, die)
# cv.createTrackbar('lval', 'settings', 0,   255, die)
# cv.createTrackbar('hhue', 'settings', 102, 255, die)
# cv.createTrackbar('hsat', 'settings', 255, 255, die)
# cv.createTrackbar('hval', 'settings', 253, 255, die)


lines = []
draw = False
newLine = False

color=(255,255,255)
pad = 15

while(True):
    _, img = cap.read()
    # img = cv.resize(img, (1920,1010), interpolation=cv.INTER_LINEAR)
    height,width=img.shape[:2]


    img = cv.flip(img, 1)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #  Make mask

    # lhue = cv.getTrackbarPos('lhue', 'settings')
    # lsat = cv.getTrackbarPos('lsat', 'settings')
    # lval = cv.getTrackbarPos('lval', 'settings')
    # hhue = cv.getTrackbarPos('hhue', 'settings')
    # hsat = cv.getTrackbarPos('hsat', 'settings')
    # hval = cv.getTrackbarPos('hval', 'settings')

    lhue=95
    lsat=197
    lval=0 
    hhue=102
    hsat=255
    hval=253

    out = cv.inRange(hsv, np.array(
        [lhue, lsat, lval]), np.array([hhue, hsat, hval]))

    # cv.imshow('m',out) 

    # Find Center
    M = cv.moments(out)
    cursor=None
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if draw:
            if newLine:
                newLine=False
                lines.append([color])
            lines[-1].append((cX, cY))
        else:
            cursor=(cX,cY)

    img=np.full([height,width,3],(51,47,44),dtype=np.uint8)

    # Plot drawings
    for cur in lines:
        points=cur[1:]
        thisColor=cur[0]
        for i in range(1, len(points)):
            if(type(points[i]) == tuple and type(points[i-1]) == tuple):
                cv.line(img, points[i], points[i-1], thisColor, 4)

    # Plot Buttons
    if not draw:
        num=len(circles.circles)
        radius=round(((height/num)-(pad*2))/2)

        # Plot each button
        for i in range(0,num):
            current=circles.circles[i]
            
            # Find coordinates for each button
            x=round(radius+pad)
            y=round((((height/num)*i) + ((height/num)/2)))

            # If button is a color swatch...
            if current.color:
                cv.circle(img, (x,y),radius,current.color,-1)

            if(cursor):
                d=np.sqrt(((cursor[0]-x)**2)+((cursor[1]-y)**2))
                if(d<=radius):

                    # If button is a color swatch...
                    if current.color:
                        color=current.color

    # Plots cursor when not drawing.
    if(cursor):
        cv.circle(img,cursor,5,(0,0,0),-1)
        cv.circle(img,cursor,3,color,-1)
        


    cv.imshow('PSPaint', img)


    # UX
    val = cv.waitKey(1)

    if(val == ord('m')):
        lines = []
    if(val == ord(' ')):
        draw = not draw
        newLine=True
    if(val ==ord('c')):
        del lines[-1]
    if(val == ord('q')):
        break
