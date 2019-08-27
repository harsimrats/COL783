import numpy as np
import cv2 as cv
import operator
from heapq import nlargest

def readImage(imgName):
	img = cv.imread(imgName)
	for i in range(len(img)):
		for j in range(len(img[0])):
			img[i][j] = img[i][j]/8
			img[i][j] = img[i][j]*8
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

def createFinalImage(img, lookUpt):
	finalImg = img
	for i in range(len(finalImg)):
		for j in range(len(finalImg[0])):
			finalImg[i][j] = lookUpt[(finalImg[i][j][0], finalImg[i][j][1], finalImg[i][j][2])]
	return finalImg

def quantCol(k_colors, histogram):
	lookUpt = {}
	i=0
	for h in histogram.keys():
		if(i%1000 == 0):
			print(i)
		minD = findDist(h, k_colors[0])
		val = k_colors[0]
		for color in k_colors:
			d = findDist(h, color)
			if d < minD:
				minD = d
				val = color
		lookUpt[h] = val
		i += 1
	return lookUpt

def showImage(name):
	cv.imshow('img', name)
	k = cv.waitKey(0)
	if k == 27:
		cv.destroyAllWindows()

image = input("Path to image: ")
quantLevels = input("Quantisation level: ")

img = readImage(image)
imgHistogram = calHistogram(img)

k_colors = calKColors(imgHistogram, int(quantLevels))
lookUp = quantCol(k_colors, imgHistogram)
finalImg = createFinalImage(img, lookUp)
showImage(finalImg)