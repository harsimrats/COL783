from scipy.spatial import Delaunay
import numpy as np
import cv2 as cv
import pickle
import dlib

features = []
feature1 = []
feature2 = []

def equalize():
	global image1, image2
	image1 = cv.resize(image1 , (max(image1.shape[1] , image2.shape[1]) , max(image1.shape[0] , image2.shape[0])) )
	image2 = cv.resize(image2 , (max(image1.shape[1] , image2.shape[1]) , max(image1.shape[0] , image2.shape[0])) )

def mouse_callback(event, x, y, flags, params):
	if event == 1:
		global features
		features.append([x, y])

def getFeaturePoints(img):
	global features
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")	
	dets = detector(img, 1)
	for k, d in enumerate(dets):
		shape = predictor(img, d)
		for p in shape.parts():
			features.append([p.x, p.y])
	# cv.namedWindow('image', cv.WINDOW_NORMAL)
	# cv.setMouseCallback('image', mouse_callback)
	# cv.imshow('image', img)
	# cv.waitKey(0)
	# cv.destroyAllWindows()

def delauneyTriangulation():
	feature3 = feature1
	trianglePoints = Delaunay(feature3)
	return trianglePoints.simplices, feature3

def SameSide(p1,p2, a,b):
	if ((b[1]-a[1]) * (p1[0] - a[0]) + (b[0] - a[0]) * (p1[1]- a[1]))*((b[1]-a[1]) * (p2[0] - a[0]) + (b[0] - a[0]) * (p2[1]- a[1])) >= 0:
		return True
	return False

def isInside(a, b, c, p):
	if SameSide(p,a, b,c) and SameSide(p,b, a,c) and SameSide(p,c, a,b): 
		return True
	else: 
		return False

def createRect(A, B, C):
	maxX = max(max(A[0], B[0]), C[0])
	minX = min(min(A[0], B[0]), C[0])
	maxY = max(max(A[1], B[1]), C[1])
	minY = min(min(A[1], B[1]), C[1])
	points = [minX, maxX, minY, maxY]
	return points

def getPointFromImage(img, beta, gamma, triangle, f):
	a = f[triangle[0]]
	b = f[triangle[1]]
	c = f[triangle[2]]
	p = [1,1]
	p[0] = int(beta * a[0] + gamma * b[0] + (1 - beta - gamma) * c[0])
	p[1] = int(beta * a[1] + gamma * b[1] + (1 - beta - gamma) * c[1])
	return img[p[1]][p[0]]

def createMorphs(trianglePoints, f1, f2, f3, alpha, img1, img2):
	res = img1.copy()
	for triangle in trianglePoints:
		A = f3[triangle[0]]
		B = f3[triangle[1]]
		C = f3[triangle[2]]
		rectPoints = createRect(A, B, C)
		for x in range(rectPoints[0], rectPoints[1]+1):
			for y in range(rectPoints[2], rectPoints[3]+1):
				P = [x, y]
				denom = ((B[1] - C[1])*(A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1]))
				beta = ((B[1] - C[1])*(P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])) / denom
				gamma = ((C[1] - A[1])*(P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])) / denom
				lamb = 1 - beta - gamma
				if (beta >= 0 and gamma >= 0 and beta <= 1 and gamma <= 1 and lamb <= 1 and lamb >= 0):
					point2 = getPointFromImage(img2, beta, gamma, triangle, f2)
					res[y][x] = point2
	return res

image1 = cv.imread('image2.jpg')
image2 = cv.imread('image1.jpg')

equalize()

getFeaturePoints(image1)
feature1 = features.copy()
features = []
getFeaturePoints(image2)
feature2 = features.copy()
if len(feature1) != len(feature2):
	sys.exit("Marked unequal number of feature points!!")

feature1 = np.array(feature1)
feature2 = np.array(feature2)

hullIndex1 = cv.convexHull(feature1)
hullIndex2 = cv.convexHull(feature2)

hIndex1 = hullIndex1[:,0]
hIndex2 = hullIndex2[:,0]

center = np.mean(hIndex1, axis=0).astype(int)
mask = np.zeros((len(image1), len(image1[0]), 3), np.uint8)
cv.fillConvexPoly(mask, hIndex1, [255, 255, 255])

trianglePoints, feature3 = delauneyTriangulation()
res = createMorphs(trianglePoints, feature1, feature2, feature3, 1, image1, image2)
output = cv.seamlessClone(res, image1, mask, (center[0], center[1]), cv.NORMAL_CLONE)
cv.imwrite( "out.jpg", output)