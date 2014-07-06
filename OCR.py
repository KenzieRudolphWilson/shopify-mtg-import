import tesseract
import numpy as np
import cv2
import cv2.cv as cv


def giveMeText():
	api = tesseract.TessBaseAPI()
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetVariable("tessedit_char_whitelist", "abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	api.SetPageSegMode(tesseract.PSM_AUTO)
	
	image=cv.LoadImage("capture.png", cv2.CV_LOAD_IMAGE_COLOR)
	#image=cv2.imread("capture.png",0)
	#iplimage = cv.CreateImageHeader((image.shape[1],image.shape[0]), cv.IPL_DEPTH_8U, 1)
	#cv.SetData(iplimage, image.tostring(),image.dtype.itemsize*image.shape[1])
	tesseract.SetCvImage(image,api)
	text=api.GetUTF8Text()
	conf=api.AllWordConfidences()
	print "text:" + str(text)
	print "confidence:" + str(conf)
	api.End()
	return text