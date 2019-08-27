import cv2
import numpy as np
from scipy.ndimage.filters import gaussian_filter

def readGrayImage(imgName):
	img = cv2.imread(imgName)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return img

# sigma=1, k=1.6, t=0.998, e=0, phi=10
def xdog(grayImg, epsilon=0.01):
	phi = 10
	difference = dog(grayImg, 1.6, 0.998)/255
	diff = difference * grayImg

	for i in range(0, len(diff)):
		for j in range(0, len(diff[0])):
			if diff[i][j] >= epsilon:
				diff[i][j] = 1
			else:
				diff[i][j] = 1 + np.tanh(phi*(diff[i][j] - epsilon))

	return diff*255

def dog(grayImg, k, gamma):
	sigma1 = 1

	gauss1 = gaussian_filter(grayImg, sigma1)
	gauss2 = gamma*gaussian_filter(grayImg, sigma1*k)

	diffGauss = gauss1 - gauss2
	return diffGauss

def showImage(name):
	cv2.imshow('img', name)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

grayImg = readGrayImage('The-gray-level-image-Lenna.png')
result = xdog(grayImg)
showImage(result)