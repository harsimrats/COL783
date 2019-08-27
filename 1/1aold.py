import numpy as np
import cv2 as cv
import operator
from heapq import nlargest

def readImage(imgName):
	img = cv.imread(imgName)
	return img

def calHistogram(img):
	histogram = {}
	for row in img:
		for pixel in row:
			if (pixel[0], pixel[1], pixel[2]) in histogram:
				histogram[(pixel[0], pixel[1], pixel[2])] += 1
			else:
				histogram[(pixel[0], pixel[1], pixel[2])] = 0
	return histogram

def calKColors(histogram, k):
	k_largest = nlargest(k, histogram, key=histogram.get)
	return k_largest

def findDist(pixel, color):
	d = 0
	for i in range(len(pixel)):
		d += (int(pixel[i]) - int(color[i]))**2
	return d

def createFinalImage(img, k_colors):
	finalImg = img
	for i in range(len(finalImg)):
		for j in range(len(finalImg[0])):
			minD = findDist(finalImg[i][j], k_colors[0])
			val = k_colors[0]
			for color in k_colors:
				d = findDist(finalImg[i][j], color)
				if d < minD:
					minD = d
					val = color
			finalImg[i][j] = val
	return finalImg

def showImage(name):
	cv.imshow('img', name)
	cv.waitKey(0)
	cv.destroyAllWindows()


img = readImage('cat.jpg')

imgHistogram = calHistogram(img)
k_colors = calKColors(imgHistogram, 256)
finalImg = createFinalImage(img, k_colors)
showImage(finalImg)