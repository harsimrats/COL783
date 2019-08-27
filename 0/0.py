import numpy as np
import cv2 as cv

def replication(image, scale, zoomIn):
	if zoomIn == 1:
		finalImage = np.zeros((len(image)*int(scale), len(image[0])*int(scale), 3), np.uint8)
		for i in range(len(image)):
			for j in range(len(image[0])):
				i1 = scale * i
				j1 = scale * j
				for i in range(int(scale)):
					for j in range(int(scale)):
						finalImage[i1+i][j1+j] = image[i][j]

	if zoomIn == 0:
		val = float(1/scale)
		finalImage = np.zeros((int(len(image)*val+1), int(len(image[0])*val+1), 3), np.uint8)
		i1 = -1
		j1 = 0
		for i in range(0, len(image), scale):
			i1+=1
			j1 = 0
			for j in range(0, len(image[0]), scale):
				if i < len(image) and j < len(image[0]):
					finalImage[i1][j1] = image[i][j]
					j1+=1

	return finalImage

def interpolation(image, scale, zoomIn):
	if zoomIn == 1:
		finalImage = np.zeros((scale*image.shape[0],scale*image.shape[1],image.shape[2]),dtype = np.uint8)
		for i in range(0, len(image)):
			for j in range(0, len(image[0])):
				for z in range(0, scale):
					for k in range(0, scale):
						for g in range(0, 3):
							finalImage[scale*i+z,scale*j+k][g] = (int)(image[i,j][g]*(scale-z)*(scale-k) + image[i+1,j][g]*(z)*(scale-k) + image[i,j+1][g]*(scale-z)*(k) + image[i+1,j+1][g]*(z)*(k))/(scale*scale)
	else:
		finalImage = np.zeros((int(image.shape[0]/scale), int(image.shape[1]/scale), image.shape[2]),dtype = np.uint8)
		for i in range(0, int(len(image)/scale)):
			for j in range(0, int(len(image[0])/scale)):
				for g in range(0, 3):
					col = 0;
					for h in range(0,scale):
						for k in range(0,scale):
							col = col + image[i*scale+h,j*scale+k][g]
					finalImage[i,j][g] = (int)(col/(scale*scale))
	return finalImage

img = cv.imread('cat.jpg')
flag = int(input('Replication (1) or interpolation (2): '))
if flag == 1:
	final = replication(img, 4, 0)
else:
	final = interpolation(img, 5, 0)
cv.imshow('img', img)
cv.imshow('final', final)
cv.waitKey(0)
cv.destroyAllWindows()