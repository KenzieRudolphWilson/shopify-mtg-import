# -*- coding: utf-8 -*-

import numpy as np
import cv2
import OCR
import json
import buildCardSet as bc
import difflib as dl

#rectangular crop
def crop(image, x, y, length, height):
    return image[(y):(y+height), (x):(x+length)]

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
    return mostSimilarWord, bestSimilarity


def drawCaptureBox(image, x, y, length, height):
    cv2.line(image,(x, y),(x ,y + height),(0,255,0),2)
    cv2.line(image,(x ,y + height),(x + length, y + height),(0,255,0),2)
    cv2.line(image,(x + length, y + height),(x + length, y),(0,255,0),2)
    cv2.line(image,(x + length, y),(x, y),(0,255,0),2)
    return image


nameList = getNameList()

cap = cv2.VideoCapture(0)
#t = 20
thresh = True
x = 100
y = 100
length = 200
height = 50

cardHeight = 300
cardWidth = 100
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # High tech UI
    key = cv2.waitKey(1)
    if key & 0xFF == ord('w'):
        y -= 3
    if key & 0xFF == ord('s'):
        y += 3
    if key & 0xFF == ord('d'):
        x += 3
    if key & 0xFF == ord('a'):
        s -= 3
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('t'):
        t += 2
    if key & 0xFF == ord('g'):
        t -= 2
    if key & 0xFF == ord('y'):
        thresh = -thresh
    if key & 0xFF == ord('p'):
        cv2.imwrite('capture.png', croppedTop)
        textTop = OCR.giveMeText()
        print "Read Text From Top of Card:" + textTop
        mostSimilarNameTop, errorDistanceTop = findMostSimilar(textTop, nameList)
        print "Most Similar :" + mostSimilarNameTop + ", with error distance :" + str(errorDistanceTop)
        cv2.imwrite('capture.png', croppedBottom)
        textBottom = OCR.giveMeText()
        print "Read Text From Bottom of Card:" + textBottom
        mostSimilarNameBottom, errorDistanceBottom = findMostSimilar(textBottom, nameList)
        print "Most Similar :" + mostSimilarNameBottom + ", with error distance :" + str(errorDistanceBottom)

        if (mostSimilarNameTop != ''):
            if (mostSimilarNameBottom != ''):
                if (errorDistanceTop <= errorDistanceBottom):
                    print "Top is closer to a real magic card name"
                else:
                    print "Bottom is closer to a real magic card name"
            else:
                print "Bottom not found, bottom chosen"
        elif (mostSimilarNameBottom != ''):
            print "Top not found, bottom chosen"
        else:
            print "No cards detected"


    croppedTop = crop(frame, x, y, length, height)
    croppedBottom = crop(frame, x + cardWidth, y + cardHeight, length, height)
    frame = drawCaptureBox(frame, x, y, length, height)
    frame = drawCaptureBox(frame, x + cardWidth, y + cardHeight, length, height)
    
    if(thresh):
        croppedTop = cv2.cvtColor(croppedTop, cv2.COLOR_BGR2GRAY)
        croppedTop = cv2.GaussianBlur(croppedTop,(1,1),0)
        t,croppedTop = cv2.threshold(croppedTop,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        croppedBottom = cv2.cvtColor(croppedBottom, cv2.COLOR_BGR2GRAY)
        croppedBottom = cv2.GaussianBlur(croppedBottom,(1,1),0)
        t,croppedBottom = cv2.threshold(croppedBottom,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 

    croppedTop = chopOffEdges(croppedTop, 2, 2, 2, 2)
    croppedBottom = chopOffEdges(croppedBottom, 2, 2, 2, 2)
    rows,cols = croppedBottom.shape

    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    croppedBottom = cv2.warpAffine(croppedBottom, M, (cols,rows))
    cv2.imshow('frame',frame)
    cv2.imshow('croppedTop',croppedTop)
    cv2.imshow('croppedBottom',croppedBottom)





# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # High tech UI
    key = cv2.waitKey(1)
    if key & 0xFF == ord('w'):
        y -= 3
    if key & 0xFF == ord('s'):
        y += 3
    if key & 0xFF == ord('d'):
        x += 3
    if key & 0xFF == ord('a'):
        x -= 3
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


    cropped = crop(frame, x, y, length, height)
    frame = drawCaptureBox(frame, x, y, length, height)
    
    if(thresh):
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cropped = cv2.GaussianBlur(cropped,(1,1),0)
        t,cropped = cv2.threshold(cropped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
        #cropped = cv2.adaptiveThreshold(cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15, t)

    cropped = chopOffEdges(cropped, 2, 2, 2, 2)
    cv2.imshow('frame',frame)
    cv2.imshow('cropped',cropped)





# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

