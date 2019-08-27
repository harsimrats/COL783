from math import sqrt as sqrt
import heapq
import numpy as np
import cv2 as cv
import sys

KNOWN = 0
DELSIG = 1
UNKNOWN = 2

MAX = 1e7

input_image = []
mask_image = []
T = []
F = []
DEL = []
lnx=0
lny=0

def solve(y1, x1, y2, x2):
	#as from the pseudo code given in the research paper
	global lnx, lny, T, F

	if 0 <= y1 < lnx:
		if 0 <= x1 < lny:
			if 0 <=y2 < lnx:
				if 0 <= x2 <lny:
					if F[y1][x1] == KNOWN:
						if F[y2][x2] == KNOWN:
							r = sqrt(2.0 - (T[y1][x1] - T[y2][x2]) ** 2)
							s = (T[y1][x1] + T[y2][x2] - r) / 2.0
							if s >= T[y1][x1] and s >= T[y2][x2]:
								return s
							else:
								s += r
								if s >= T[y1][x1] and s >= T[y2][x2]:
									return s
						else:
							return 1.0 + T[y1][x1]	
					elif F[y2][x2] == KNOWN:
						return 1.0 + T[y2][x2]
	return MAX

def grady(y, x):
	global lnx, lny, T, F
	tyx = T[y, x]
	
	if 1 <= y < lnx-1:
		if F[y - 1][x] != UNKNOWN and F[y + 1][x] != UNKNOWN:
			return (T[y + 1][x] - T[y - 1][x]) / 2.0
		elif F[y + 1][x] != UNKNOWN:
			return T[y + 1][x] - tyx
		elif F[y - 1][x] != UNKNOWN:
			return tyx - T[y - 1][x]
		else:
			return 0.0
	else:
		return MAX

def gradx(y, x):
	global lnx, lny, T, F
	tyx = T[y, x]
	
	if 1 <= x < lny-1:
		if F[y, x - 1] != UNKNOWN and F[y, x + 1] != UNKNOWN:
			return (T[y, x + 1] - T[y, x-1]) / 2.0
		elif F[y, x + 1] != UNKNOWN:
			return T[y, x+1] - tyx
		elif F[y, x - 1] != UNKNOWN:
			return tyx - T[y, x-1]
		else:
			return 0.0
	else:
		return MAX

def single_inpaint(y, x, radius):
	global lnx, lny, T, F, input_image
	image = input_image
	
	pixel_sum = np.zeros((3), dtype=float)
	weight_sum = 0.0
	d0 = 1.0
	t0 = 1.0
	for nb_y in range(y - radius, y + radius + 1):
		if 0 <= nb_y < lnx:
			for nb_x in range(x - radius, x + radius + 1):
				if 0 <= nb_x < lny:
					if ((y-nb_y) ** 2 + (x-nb_x) ** 2) <= (radius ** 2):
						if F[nb_y, nb_x] != UNKNOWN:
	
							dst = d0*d0 / ((y-nb_y)**2 + (x-nb_x)**2)
							dirr = max(1e-7 , abs((y-nb_y)*grady(y,x) + (x-nb_x) * gradx(y,x))/sqrt((y-nb_y)**2 + (x-nb_x)**2)) 
							lev = t0 / (1.0 + abs(T[y][x] - T[nb_y][nb_x]))

							weight = dirr * dst * lev

							pixel_sum[0] += weight * image[nb_y][nb_x][0]
							pixel_sum[1] += weight * image[nb_y][nb_x][1]
							pixel_sum[2] += weight * image[nb_y][nb_x][2]

							weight_sum += weight

	return pixel_sum / weight_sum

def inpaint(image, mask):
	global lnx, lny, T, F, DEL
	radius = 5
	lnx = len(image)
	lny = len(image[0])

	#initialise
	T = np.full((lnx, lny), MAX, dtype=float)
	F = mask.astype(int)
	F[F == 1] = 2
	DEL = []

	mnzx, mnzy = mask.nonzero()

	for y,x in zip(mnzx, mnzy):
		for nb_y, nb_x in [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]:
			if 0 <= nb_y < lnx:
				if 0 <= nb_x < lny:
					if F[nb_y][nb_x] == UNKNOWN or F[nb_y][nb_x] == KNOWN:
						if mask[nb_y][nb_x] == 0:
							heapq.heappush(DEL, (0.0, nb_y, nb_x))
							T[nb_y][nb_x] = 0.0
							F[nb_y][nb_x] = DELSIG

	#pseudo-code as from the paper
	while True :
		if len(DEL) == 0:
			break
		z, y, x = heapq.heappop(DEL)
		F[y][x] = KNOWN
		
		for nb_y, nb_x in [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]:
			if 0 <= nb_y < lnx:
				if 0 <= nb_x < lny:
					if F[nb_y, nb_x] == UNKNOWN:
						t1 = solve(nb_y - 1, nb_x, nb_y, nb_x - 1)
						t2 = solve(nb_y + 1, nb_x, nb_y, nb_x + 1)
						t3 = solve(nb_y - 1, nb_x, nb_y, nb_x + 1)
						t4 = solve(nb_y + 1, nb_x, nb_y, nb_x - 1)
						
						t = min(t1, t2, t3, t4)
						T[nb_y][nb_x] = t
						pixel_vals = single_inpaint(nb_y, nb_x, radius)

						image[nb_y][nb_x][0] = pixel_vals[0]
						image[nb_y][nb_x][1] = pixel_vals[1]
						image[nb_y][nb_x][2] = pixel_vals[2]
						F[nb_y][nb_x] = DELSIG
						heapq.heappush(DEL, (t, nb_y, nb_x))

def show_image(image):
	cv.namedWindow('filter', cv.WINDOW_NORMAL)
	cv.imshow('filter', image)
	key = cv.waitKey(0)
	if key == 27:
		cv.destroyAllWindows()


input_image = cv.imread('lena_in.png')
mask_image = cv.imread('lena_mask.png')

if(len(input_image) != len(mask_image)):
	sys.exit("Image and mask dimensions inconsistent")
if(len(input_image[0]) != len(mask_image[0])):
	sys.exit("Image and mask dimensions inconsistent")

mask_image = mask_image[:, :, 1].astype(bool)

inpaint(input_image, mask_image)
final_image = input_image.copy()
show_image(final_image)