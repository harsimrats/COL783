import numpy as np
import cv2 as cv
import operator
from heapq import nlargest

class kdTree():
	def __init__(self, rootid):
		self.left = None
		self.right = None
		self.rootid = rootid

def get_leaf_nodes(node):
	leafs = []
	if node is not None:
		if node.left is None and node.right is None:
			leafs.append(node.rootid)
		leafs += get_leaf_nodes(node.left) + get_leaf_nodes(node.right)
	return leafs

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

def showImage(name):
	cv.imshow('Quantised Image', name)
	k = cv.waitKey(0)
	if k == 27:
		cv.destroyAllWindows()

def growTree(points, k):

	if k == 1:
		return  None

	var = (np.var(points, axis=0)).tolist()
	ind = var.index(max(var))
	med = (np.median(points, axis=0))[ind]

	root = kdTree(med)
	left = [x for x in points if x[ind] < med]
	right = [x for x in points if x[ind] >= med]

	if k/2 != 1:
		root.left = growTree(left, k/2)
		root.right = growTree(right, k-k/2)
	else:
		avg = [0,0,0]
		for i in range(0, len(points)):
				avg += points[i]
		avg = avg/float(len(points))

		root.rootid = avg

	return root

def findKColors(image, K):
	lst = []
	for i in range(0, len(image)):
		for j in range(0, len(image[0])):
			lst.append(image[i][j])
	tree = growTree( lst , K)

	kColors = get_leaf_nodes(tree)

	return kColors

def findDist(pixel, color):
	d = 0
	for i in range(len(pixel)):
		d += (int(pixel[i]) - int(color[i]))**2
	return d

def quantise(k_colors, histogram):
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

def createFinalImage(img, lookUpt):
	finalImg = img
	for i in range(len(finalImg)):
		for j in range(len(finalImg[0])):
			finalImg[i][j] = lookUpt[(finalImg[i][j][0], finalImg[i][j][1], finalImg[i][j][2])]
	return finalImg

image_path = input("Path to image: ")
k = int(input("Quantisation level: "))

image = readImage(image_path)
histogram = calHistogram(image)
k_colors = findKColors(image, k)
lookUpt = quantise(k_colors, histogram)
finalImg = createFinalImage(image, lookUpt)
showImage(finalImg)

# # r = []
# # g = []
# # b = []
# # for i in range(0, len(finalImg)):
# # 	for j in range(0, len(finalImg[0])):
# # 		r.append(finalImg[0])
# # 		g.append(finalImg[1])
# # 		b.append(finalImg[2])
		
# Hdat = []
# Ldat = []
# Sdat = []    
# for row in finalImg:
# 	for pixel in row:
# 		h,l,s = colorsys.rgb_to_hls(pixel[0]/255., pixel[1]/255., pixel[2]/255.)
# 		Hdat.append(int(h*255.))
# 		Ldat.append(int(l*255.))
# 		Sdat.append(int(s*255.))

# r.putdata(Hdat)
# g.putdata(Ldat)
# b.putdata(Sdat)
# newimg = Image.merge('RGB',(r,g,b))
# newimg.save('lenaHSV.png')