import numpy as np
import cv2 as cv
import colorsys
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.neighbors import KDTree
# import nmslib

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

def luminamceRemapping(A, ADash, B):
	meanA = np.mean(A)
	meanB = np.mean(B)
	sdA = np.std(A)
	sdB = np.std(B)
	A = (sdB/sdA) * ( A - meanA) + meanB
	ADash = (sdB/sdA) * ( ADash - meanA) + meanB
	return A, ADash, B

def convertToYIQ(img):
	convertedImg = np.zeros((len(img), len(img[0]), 3))
	for i in range(0, len(img)):
		for j in range(0, len(img[0])):
			convertedImg[i][j] = list(colorsys.rgb_to_yiq(img[i][j][0], img[i][j][1], img[i][j][2]))
	return convertedImg

def convertToRGB(img):
	convertedImg = np.zeros((len(img), len(img[0]), 3))
	for i in range(0, len(img)):
		for j in range(0, len(img[0])):
			convertedImg[i][j] = list(colorsys.yiq_to_rgb(img[i][j][0], img[i][j][1], img[i][j][2]))
	return convertedImg

def computeWeights(num_ch, last=False):
	s = np.zeros((3, 3, num_ch))
	l = np.zeros((5, 5, num_ch))
	x, y = np.mgrid[-3 // 2 + 1 : 3 // 2 + 1, -3 // 2 + 1 : 3 // 2 + 1]
	g = np.exp(-((x ** 2 + y ** 2) / (2.0 * 0.5 ** 2)))
	gS = g/g.sum()
	x, y = np.mgrid[-5 // 2 + 1 : 5 // 2 + 1, -5 // 2 + 1 : 5 // 2 + 1]
	g = np.exp(-((x ** 2 + y ** 2) / (2.0 * 1 ** 2)))
	gL = g/g.sum()
	for i in range(num_ch):
		s[:, :, i] = gS
		l[:, :, i] = gL

	flattenS = s.flatten()
	flattenL = l.flatten()
	wS = (1 / (9 * num_ch)) * flattenS
	wL = (1 / (25 * num_ch)) * flattenL
	wH = (1 / 12 * num_ch) * flattenL[: 12 * num_ch]
	if not last:
		return np.hstack([wS, wL, wS, wH])
	else:
		return np.hstack([wL, wH])

def createFeatureVector(GP, num_ch, full=True):
	featureVector = []
	paddedGP = np.pad(GP[0], ((2, 2), (2, 2), (0, 0)), mode='symmetric')

	for i in range(len(GP)):
		if i == 0:
			firstFeature = extract_patches_2d(paddedGP, (5, 5))
			if not full:
				firstFeature = firstFeature.reshape((firstFeature.shape[0], -1))[:, : 12 * num_ch]
			else:
				firstFeature = firstFeature.reshape((firstFeature.shape[0], -1))
			featureVector.append(firstFeature)

		else:
			paddedGP = np.pad(GP[i], ((2, 2), (2, 2), (0, 0)), mode='symmetric')
			pyr_pads = np.pad(GP[i - 1], ((1, 1), (1, 1), (0, 0)), mode='symmetric')

			l = extract_patches_2d(paddedGP, (5, 5))
			s = extract_patches_2d(pyr_pads, (3, 3))
			num_ft = (9 + 25) * num_ch

			if not full:
				s = s.reshape((s.shape[0], -1))
				l = l.reshape((l.shape[0], -1))[:, : 12 * num_ch]
				num_ft = (9 + 12) * num_ch
			else:
				s = s.reshape((s.shape[0], -1))
				l = l.reshape((l.shape[0], -1))

			levelFeatures = np.zeros((len(GP[i]) * len(GP[i][0]), num_ft))
			for x in range(len(GP[i])):
				for y in range(len(GP[i][0])):
					levelFeatures[x * len(GP[i][0]) + y] = np.hstack((s[x // 2 * int(np.ceil(len(GP[i][0]) / 2)) + y // 2], l[x * len(GP[i][0]) + y]))

			featureVector.append(levelFeatures)

	return featureVector

def bestCoherenceMatch(data, point, loc, data_size, S):
	minDist = float('inf')
	bestI = -1
	bestJ = -1

	startI = max(0, loc[0] - 2)
	endI = min(len(S), loc[0] + 3)
	startJ = max(0, loc[1] - 2)
	endJ = loc[1] + 1
	for i in range(startI, endI):
		for j in range(startJ, endJ):
			if i == loc[0] and j == loc[1]:
				break
			else:
				tempI = S[i, j, 0] + (loc[0] - i)
				tempJ = S[i, j, 1] + (loc[1] - j)

				if tempI >= 0:
					if tempI < data_size[0]:
						if tempJ >= 0:
							if tempJ < data_size[1]:
								dist = np.linalg.norm(data[tempI * data_size[1] + tempJ] - point)
								if dist < minDist:
									bestJ = tempJ
									bestI = tempI
									minDist = dist

	return bestI * data_size[1] + bestJ

def imageAnalogy(originalA, originalADash, originalB):
	A = convertToYIQ(originalA)
	ADash = convertToYIQ(originalADash)
	B = convertToYIQ(originalB)

	A, ADash, B = luminamceRemapping(A, ADash, B)

	num_ch = A.shape[2]
	num_levels = 3
	GPA = createGaussianPyramid(A, num_levels)
	GPADash = createGaussianPyramid(ADash, num_levels)
	GPB = createGaussianPyramid(B, num_levels)

	featureVectorA = createFeatureVector(GPA, num_ch, False)
	featureVectorB = createFeatureVector(GPB, num_ch, False)
	featureVectorADash = createFeatureVector(GPADash, num_ch, True)

	weights = computeWeights(num_ch)
	weights_last = computeWeights(num_ch, last=True)
	k = 2 * (pow(2, -num_levels))

	GPBDash = []
	for i in range(0, num_levels + 1):
		paddedBDashL = np.zeros((len(GPB[i]) + 4, len(GPB[i][0]) + 4, num_ch))
		S = -1 * np.ones((len(GPB[i]), len(GPB[i][0]), 2), dtype=int)
		data = np.hstack((featureVectorA[i], featureVectorADash[i]))

		w = weights
		if i == 0:
			w = weights_last
		else:
			paddedGPBDash = np.pad(GPBDash[i - 1], ((1, 1), (1, 1), (0, 0)), mode='symmetric')

		for x in range(len(GPB[i])):
			for y in range(len(GPB[i][0])):
				if i != 0:
					temp = paddedBDashL[x : x + 5][ y : y + 5][ :]
					temp1 = temp.flatten()
					BDashL = temp1[: 12 * num_ch]
					temp2 = paddedGPBDash[int(x / 2) : int(x / 2 + 3)][ int(y / 2) : int(y / 2 + 3)][ :]
					BDashS = temp2.flatten()
					B_ftp = np.hstack((featureVectorB[i][x * len(GPB[i][0]) + y], BDashS, BDashL))
				else:
					temp = paddedBDashL[x : x + 5][ y : y + 5][ :]
					temp1 = temp.flatten()
					initialBDash = temp1[: 12 * num_ch]
					B_ftp = np.hstack((featureVectorB[i][x * len(GPB[i][0]) + y], initialBDash))

				newB = np.reshape(B_ftp, (len(B_ftp), 1))
				tree = KDTree(newB, leaf_size=40)
				dist, ann = tree.query(newB, k=1)
				ann = np.array([ann[len(ann)-1]])
				coh = bestCoherenceMatch(data, B_ftp, (x, y), (len(GPA[i]), len(GPA[i][0])), S)

				# print(np.array(ann).shape, ann, coh )

				if coh >= 0:
					d_coh = np.linalg.norm(( data[coh] - B_ftp) * w)
					d_app = np.linalg.norm((data[ann] - B_ftp) * w)

					if d_coh <= d_app * (1 + k):
						match_i = coh // len(GPA[i][0])
						match_j = coh % len(GPA[i][0])
					else:
						match_i = ann // len(GPA[i][0])
						match_j = ann % len(GPA[i][0])
				else:
					match_i = ann // len(GPA[i][0])
					match_j = ann % len(GPA[i][0])

				# print(np.array(paddedBDashL).shape, np.array(GPADash[i]).shape, match_i, match_j)
				paddedBDashL[x + 2, y + 2] = GPADash[i][match_i, match_j]
				S[x][y][0] = match_i
				S[x][y][1] = match_j

		GPBDash.append(paddedBDashL[2 : 2 + len(GPB[i]), 2 : 2 + len(GPB[i][0])])
		k = k * 2

	B_im = convertToRGB(B_im)
	B_yiq = np.dstack((GPBDash[-1][:, :, 0], B_im[:, :, 1], B_im[:, :, 2]))
	return convertToRGB(B_yiq)

originalA = cv.imread("A.jpg")
originalADash = cv.imread("Ad.jpg")
originalB = cv.imread("B.jpg")

BDash = imageAnalogy(originalA, originalADash, originalB)
showImage(BDash)