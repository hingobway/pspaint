import circles
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import time
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
import os
from dotenv import load_dotenv
load_dotenv()


cloudinary.config(
    cloud_name='pspaint',
    api_key=os.getenv('CKEY'),
    api_secret=os.getenv('CSECRET')
)

cap = cv.VideoCapture(0)


def die(*arg):
    pass


def plotLink(img, id):
    link = 'pspaint.xyz/i/' + id
    pos = (165, 450)
    size = 1.5
    thick = 4
    cv.putText(img, link, pos, cv.FONT_HERSHEY_SIMPLEX,
               size, (0, 0, 0), (thick+2), cv.LINE_AA)
    cv.putText(img, link, pos, cv.FONT_HERSHEY_SIMPLEX,
               size, (255, 255, 255), thick, cv.LINE_AA)


def saveImage(img):
    ts = str(int(time.time()))
    fname = "assets/picture" + ts + '.jpg'
    cv.imwrite(fname, img)
    resp = cloudinary.uploader.upload(fname)
    url = resp['secure_url']
    r = requests.post('https://pspaint.xyz/api/upload',
                      data={'url': url, 'timestamp': ts})
    # r = requests.post('http://localhost:5000/api/upload', data = {'url':url, 'timestamp':ts})
    if(r.status_code is not 200):
        # freak out
        pass
    os.remove(fname)
    return r.json()['snow']


# cv.namedWindow('settings')
# cv.createTrackbar('lhue', 'settings', 95,  255, die)
# cv.createTrackbar('lsat', 'settings', 197, 255, die)
# cv.createTrackbar('lval', 'settings', 0,   255, die)
# cv.createTrackbar('hhue', 'settings', 102, 255, die)
# cv.createTrackbar('hsat', 'settings', 255, 255, die)
# cv.createTrackbar('hval', 'settings', 253, 255, die)


lines = []
draw = False
save = False
newLine = False
oldImg = None

color = (255, 255, 255)
pad = 15
curBG = 0

frame = None

while(True):
    _, img = cap.read()
    orig = img
    # img = cv.resize(img, (1920,1010), interpolation=cv.INTER_LINEAR)
    height, width = img.shape[:2]

    img = cv.flip(img, 1)

    try:
        frame = cv.imread('assets/cur.jpg')
    except:
        pass

    backgrounds = [img, np.full([height, width, 3], (51, 47, 44), dtype=np.uint8), (frame if (
        frame is not None) else np.full([height, width, 3], (0, 0, 0), dtype=np.uint8))]

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #  Make mask

    # lhue = cv.getTrackbarPos('lhue', 'settings')
    # lsat = cv.getTrackbarPos('lsat', 'settings')
    # lval = cv.getTrackbarPos('lval', 'settings')
    # hhue = cv.getTrackbarPos('hhue', 'settings')
    # hsat = cv.getTrackbarPos('hsat', 'settings')
    # hval = cv.getTrackbarPos('hval', 'settings')

    # # Med Glove
    # lhue = 95
    # lsat = 197
    # lval = 0
    # hhue = 102
    # hsat = 255
    # hval = 253

    # Orange Finger
    lhue = 5
    lsat = 102
    lval = 195
    hhue = 25
    hsat = 190
    hval = 255

    # # Phone Blob
    # lhue = 98
    # lsat = 91
    # lval = 215
    # hhue = 107
    # hsat = 162
    # hval = 255

    # # Phone Blob 2
    # lhue = 86
    # lsat = 86
    # lval = 179
    # hhue = 104
    # hsat = 157
    # hval = 255

    out = cv.inRange(hsv, np.array(
        [lhue, lsat, lval]), np.array([hhue, hsat, hval]))

    # SHOW MASK FOR CONFIG
    # cv.imshow('m', out)

    # Find Center
    M = cv.moments(out)
    cursor = None
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if draw:
            if newLine:
                newLine = False
                lines.append([color])
            lines[-1].append((cX, cY))
        else:
            cursor = (cX, cY)

    # img=np.full([height,width,3],(51,47,44),dtype=np.uint8)
    img = backgrounds[curBG]
    unedited = frame

    # Plot drawings
    for cur in lines:
        points = cur[1:]
        thisColor = cur[0]
        for i in range(1, len(points)):
            if(type(points[i]) == tuple and type(points[i-1]) == tuple):
                cv.line(img, points[i], points[i-1], thisColor, 4)

    # Plot Buttons
    if not draw and not save:
        # Plot the last image link
        if(oldImg is not None):
            plotLink(img, oldImg)

        # Plot each button
        num = len(circles.circles)
        radius = round(((height/num)-(pad*2))/2)
        for i in range(0, num):
            current = circles.circles[i]

            # Find coordinates for the button
            x = round(radius+pad)
            y = round((((height/num)*i) + ((height/num)/2)))

            # Draw
            current.draw(img, x, y, radius)

            if(cursor):
                d = np.sqrt(((cursor[0]-x)**2)+((cursor[1]-y)**2))
                if(d <= radius):

                    # If button is a color swatch...
                    if current.color:
                        color = current.color

    # Plots cursor when not drawing.
    if(cursor and (not save)):
        cv.circle(img, cursor, 5, (0, 0, 0), -1)
        cv.circle(img, cursor, 3, color, -1)

    cv.imshow('PSPaint', img)

    if(save):
        save = False
        oldImg = saveImage(img)

    # UX
    val = cv.waitKey(1)

    if(val == ord('q')):
        lines = []
    if(val == ord('d')):
        if(oldImg is not None):
            oldImg = None
        draw = not draw
        newLine = True
    if(val == ord('v')):
        if not draw:
            del lines[-1]
    if(val == ord('e')):
        if(curBG < (len(backgrounds)-1)):
            curBG = curBG+1
        else:
            curBG = 0
    if(val == ord('r')):
        orig = cv.flip(orig, 1)
        cv.imwrite('assets/cur.jpg', orig)
        curBG = 2
    if(val == ord('a')):
        draw = False
        if(not save):
            save = True
    if(val == ord('z') or val == ord('n')):
        break
