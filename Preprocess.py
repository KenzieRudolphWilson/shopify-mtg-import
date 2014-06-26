# -*- coding: utf-8 -*-

import numpy as np
import cv2
import OCR
import json

def checkForCard(text):
    jsonData = open('AllSetsArray.json')
    data = json.load(jsonData)
    jsonData.close()

    

cap = cv2.VideoCapture(0)
t = 20
thresh =1
canny = 1
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    try:
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
    	pass

    minLineLength = 200
    maxLineGap = 20
    x1 = 0
    y1 = 0
    x2 = 380
    y2 = 0
    x3 = 380
    y3 = 50
    x4 = 0
    y4 = 50
    x = 63
    y = 60
    cv2.line(frame,(x + x1,y + y1),(x + x2,y + y2),(0,255,0),2)
    cv2.line(frame,(x + x2,y + y2),(x + x3,y + y3),(0,255,0),2)
    cv2.line(frame,(x + x3,y + y3),(x + x4,y + y4),(0,255,0),2)
    cv2.line(frame,(x + x4,y + y4),(x + x1,y + y1),(0,255,0),2)
    #lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
    #if lines is not None:
    #	for x1, y1, x2, y2 in lines[0]:
    #		cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('edges',edges)
    cropped = frame[(y+y1):(y+y3), (x+x1):(x+x2)]
	
    if(thresh > 0):
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)    
    	cropped = cv2.adaptiveThreshold(cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15, t)

    cropped = cropped[(2):(y3-2), (2):(x2-2)]

    cv2.imshow('cropped',cropped)


    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('t'):
        t += 2
    if key & 0xFF == ord('g'):
        t -= 2
    if key & 0xFF == ord('y'):
    	thresh = -thresh
    if key & 0xFF == ord('p'):
        cv2.imwrite('capture.png', cropped)
        checkForCard(OCR.giveMeText())


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


