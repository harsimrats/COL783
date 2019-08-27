import numpy as np
import cv2 as cv
from scipy import sparse
from scipy.sparse import linalg

class SeamlessEditingTool:
	def __init__(self, ref, target, mask):
		self.ref = ref
		self.target = target
		self.mask = mask
		self.height, self.width, blank = self.ref.shape
		self.newImage = np.zeros([self.height, self.width])
		
		self.maskidx2Corrd = []
		self.Coord2indx = -1 * np.ones([self.height, self.width])

		self.if_strict_interior = []  # left, right, top, botton
		idx = 0

		for i in range(self.height):
			for j in range(self.width):
				if self.mask[i][j][0] == 255:
					self.maskidx2Corrd.append([i, j])
					self.if_strict_interior.append([
						i > 0 and self.mask[i - 1, j, 0] == 255,
						i < self.height - 1 and self.mask[i + 1, j, 0] == 255,
						j > 0 and self.mask[i, j - 1, 0] == 255,
						j < self.width - 1 and self.mask[i, j + 1, 0] == 255
					])
					self.Coord2indx[i][j] = idx
					idx += 1

		N = idx
		self.b = np.zeros([N, 3])
		self.A = np.zeros([N, N])

	
	def create_possion_equation(self):
		N = self.b.shape[0]
		for i in range(N):
			self.A[i][i] = 4
			x, y = self.maskidx2Corrd[i]
			if self.if_strict_interior[i][0]:
				self.A[i, int(self.Coord2indx[x - 1, y])] = -1
			if self.if_strict_interior[i][1]:
				self.A[i, int(self.Coord2indx[x + 1, y])] = -1
			if self.if_strict_interior[i][2]:
				self.A[i, int(self.Coord2indx[x, y - 1])] = -1
			if self.if_strict_interior[i][3]:
				self.A[i, int(self.Coord2indx[x, y + 1])] = -1


		self.A = sparse.lil_matrix(self.A, dtype=int)
		for i in range(N):
			flag = np.mod(
				np.array(self.if_strict_interior[i], dtype=int) + 1, 2)
			x, y = self.maskidx2Corrd[i]
			for j in range(3):
				self.b[i, j] = 4 * self.ref[x, y, j] - self.ref[x - 1, y, j] - \
					self.ref[x + 1, y, j] - self.ref[x,
													 y - 1, j] - self.ref[x, y + 1, j]
				self.b[i, j] += flag[0] * self.target[x - 1, y, j] + \
					flag[1] * self.target[x + 1, y, j] + flag[2] * \
					self.target[x, y - 1, j] + \
					flag[3] * self.target[x, y + 1, j]

	def possion_solver(self):

		self.create_possion_equation()
		
		x_r = linalg.cg(self.A, self.b[:, 0])[0]
		x_g = linalg.cg(self.A, self.b[:, 1])[0]
		x_b = linalg.cg(self.A, self.b[:, 2])[0]

		self.newImage = self.target

		for i in range(self.b.shape[0]):
			x, y = self.maskidx2Corrd[i]
			self.newImage[x, y, 0] = np.clip(x_r[i], 0, 255)
			self.newImage[x, y, 1] = np.clip(x_g[i], 0, 255)
			self.newImage[x, y, 2] = np.clip(x_b[i], 0, 255)

		return self.newImage

def seamless(ref, target, mask, center):
	tools = SeamlessEditingTool(ref, target, mask)
	newImage = tools.possion_solver()
	return newImage