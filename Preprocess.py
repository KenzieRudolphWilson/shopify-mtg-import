# -*- coding: utf-8 -*-

import numpy as np
import cv2
import OCR
import json
import buildCardSet as bc
import difflib as dl

#rectangular crop
def crop(image, x, y, length, height):
    return image[(x):(x+length), (y):(y+height)]

#removes pixels from each edge
def chopOffEdges(image, left, right, top, bottom):
    return image[(left):(len(image[0]) - right), (top):(len(image[1]) - bottom)]

def getNameList():
    try:
        jsonData = open('cardNameSet.json')
        data = json.load(jsonData)
        jsonData.close()
    except IOError:
        jsonData = bc.generateCardMap
        bc.saveUTF8File(jsonData, 'cardNameSet.json')
        data = json.loads(jsonData)
    return list(data)


def findMostSimilar(imageText, vocabulary):
    bestSimilarity = 0
    mostSimilarWord = ''
    for word in vocabulary:
        seq = dl.SequenceMatcher(None, imageText, word)
        similarity = seq.ratio()
        if similarity > bestSimilarity:
            bestSimilarity = similarity
            mostSimilarWord = word
    return mostSimilarWord


def drawCaptureBox(image, x, y, length, height):
    cv2.line(image,(x, y),(x ,y + height),(0,255,0),2)
    cv2.line(image,(x ,y + height),(x + length, y + height),(0,255,0),2)
    cv2.line(image,(x + length, y + height),(x + length, y),(0,255,0),2)
    cv2.line(image,(x + length, y),(x, y),(0,255,0),2)
    return image


def checkForCard(text, names):
    return findMostSimilar(text, names)
    


nameList = getNameList()

cap = cv2.VideoCapture(0)
t = 20
thresh =1
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    try:
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
    	pass

    
    #cv2.imshow('edges',edges)
    x = 100
    y = 100
    length = 200
    height = 50
    cropped = crop(frame, x, y, length, height)
    frame = drawCaptureBox(frame, x, y, length, height)
	
    if(thresh > 0):
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)    
    	cropped = cv2.adaptiveThreshold(cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15, t)

    cropped = chopOffEdges(cropped, 2, 2, 2, 2)
    cv2.imshow('frame',frame)
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
        text = OCR.giveMeText()
        print "Read Text :" + text
        print "Most Similar :" + checkForCard(text, nameList)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


