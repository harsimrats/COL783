import numpy as np
import cv2 as cv
from heapq import nlargest

def showImage(name):
	cv.imshow('img.jpg', name)
	k = cv.waitKey(0)
	if k == 27:
		cv.destroyAllWindows()

def createGaussianPyramid (image1, numPyramids):
	GaussianPyramid = []

	original = image1
	for n in range(numPyramids):
		res = cv.GaussianBlur(original,(5,5),0)
		final = cv.resize(res,(len(res[0])//2,len(res)//2))
		GaussianPyramid.append(final)
		original = final.copy()
	return GaussianPyramid

def createLaplacianPyramid(image1, GaussianPyramid):
	LaplacianPyramid = []
	
	for i in range(1, len(GaussianPyramid)):
		img = cv.resize(GaussianPyramid[i],(len(GaussianPyramid[i-1][0]),len(GaussianPyramid[i-1])))
		LaplacianPyramid.append(GaussianPyramid[i-1].astype(int) - img.astype(int))

	return LaplacianPyramid

def interpolation(image, scale, zoomIn):
	if zoomIn == 1:
		finalImage = np.zeros((scale*len(image), scale*len(image[0]), 3), dtype =int)
		for x in range(0, len(image)-1):
			for y in range(0, len(image[0])-1):
				for z in range(0, scale):
					for k in range(0, scale):
						for g in range(0, 3):
							finalImage[scale*x+z , scale*y+k][g] = (int)(image[x,y][g]*(scale-z)*(scale-k) + 
																		image[x+1,y][g]*(z)*(scale-k) + 
																		image[x,y+1][g]*(scale-z)*(k) + 
																		image[x+1,y+1][g]*(z)*(k))/(scale*scale)
	else:
		finalImage = np.zeros((int(len(image)/scale), int(len(image[0])/scale), 3), dtype =int)
		for i in range(0, int(len(image)/scale)):
			for j in range(0, int(len(image[0])/scale)):
				for g in range(0, 3):
					col = 0;
					for h in range(0,scale):
						for k in range(0,scale):
							col += image[i*scale+h,j*scale+k][g]
					finalImage[i,j][g] = (int)(col/(scale*scale))
	return finalImage

###########################################################
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

def compress(img, GP, LP):
	# The original image Io can be completely recovered from level In and the Laplace levels Lo, ... ,Ln - 1 by quantizing the pixel values and adding them
	blendedLP = []
	for i in range(len(LP)):
		blendedLP.append(LP[i])
	blendedLP.append(GP[len(GP)-1])

	re = np.zeros(img.shape, dtype = int)
	for i in range(0, len(blendedLP)):
		if i == len(blendedLP) - 1:
			temp = interpolation(blendedLP[i], pow(2, i+1), 1)
			temp += re[:len(temp), :len(temp[0]), :]
		else:
			imgHistogram = calHistogram(blendedLP[i])
			k_colors = calKColors(imgHistogram, 2) # 200 for apple, >1000 for lenna
			lookUp = quantCol(k_colors, imgHistogram)
			finalImg = createFinalImage(blendedLP[i], lookUp)
			re += interpolation(finalImg, pow(2, i+1), 1)

	re1 = temp[:len(temp[0])-pow(2, len(blendedLP)), :len(temp)-pow(2, len(blendedLP)), :]
	cv.imwrite("compress.png", re)

# image = cv.imread('lenna1.png')
# GP = createGaussianPyramid(image, 2)
# LP = createLaplacianPyramid(image, GP)
# compress(image, GP, LP)

##############################################################

def combine2Images(image1, image2):
	c = np.zeros((len(image1), len(image1[0]), 3))
	for i in range(len(image1)):
		for j in range(len(image1[0])):
			if j < len(image1[0])//2:
				c[i][j] = image1[i][j]
			else:
				c[i][j] = image2[i][j]
	return c

def mosaic(image1, image2, LP1, LP2, GP1, GP2):
	blendedLP = []
	for i in range(len(LP1)):
		blendedLP.append(combine2Images(LP1[i], LP2[i]).copy())
	blendedLP.append(combine2Images(GP1[len(GP1)-1], GP2[len(GP1)-1]).copy())

	re = np.zeros(image1.shape, dtype = int)
	for i in range(0, len(blendedLP)):
		re += interpolation(blendedLP[i], pow(2, i+1), 1)

	re1 = re[:len(re[0])-pow(2, len(blendedLP)), :len(re)-pow(2, len(blendedLP)), :]

	showImage(re1.astype('uint8'))

image1 = cv.imread('a.jpg')
image2 = cv.imread('o.jpg')

GP1 = createGaussianPyramid(image1, 4)
LP1 = createLaplacianPyramid(image1, GP1)
GP2 = createGaussianPyramid(image2, 4)
LP2 = createLaplacianPyramid(image2, GP2)

mosaic(image1, image2, LP1, LP2, GP1, GP2)
#################################################################