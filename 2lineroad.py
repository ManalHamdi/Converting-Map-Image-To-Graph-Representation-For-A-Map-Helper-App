import cv2
import numpy as np

input_image = cv2.imread('aui no legend.png') #reads the image as an ndarray

bgr = [253, 253, 253]
thresh = 2
 
minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh]) 
binary_image = cv2.inRange(input_image, minBGR, maxBGR) #inrange: if a pixel is within the range specified by minBGR and maxBGR it is set to 255 (1) otherwise 0
image = cv2.bitwise_and(input_image, input_image, mask = binary_image)

copy = image.copy()
double_pixel = copy.copy()

for i in range (0, double_pixel.shape[0] ):
	for j in range(0, double_pixel.shape[1] ):
		double_pixel[i,j] = [0,0,0]
petitgrey = np.array([220, 220, 220], np.int32)
grandgrey = np.array([237, 237, 237], np.int32)

t1 = [240, 240, 240] #this represents the min of road color
t2 = [255, 255, 255] #this represents the max of road color

'''
This step looks for grey pixels (background) and see if they have white pixels (road pixels) as a neighbour, 
if it s the case we make the grey pixel white and the road pixel black
We do all of this to 2 road line 
'''
for i in range (1, copy.shape[0] - 1):
	for j in range(1, copy.shape[1] - 1):
		if ((input_image[i][j] <= grandgrey).all() and (input_image[i][j] >= petitgrey).all()):
			for a in range(-1,2):
				for b in range(-1,2):
					if (((input_image[i+a, j+b] <= t2).all() and (input_image[i+a, j+b] >= t1).all()) and (a != 0 or b != 0)):
						double_pixel[i, j] = [255,255,255]
						double_pixel[i+a, j+b] = [255,255,255]
"""copy2 = double_pixel.copy()
for i in range (1, rows - 1):
	for j in range(1, columns - 1):
		if ((double_pixel[i, j] == [0,0,0]).all()):
			flag = False
			for a in range(-1,2):
				for b in range(-1,2):
					if ((double_pixel[i+a, j+b] == [255,255,255]).all()):
						flag = True
			if (flag == True):
				copy2[i,j] =  [255,255,255]"""

cv2.imwrite('AuiNoLegendDouble.png', double_pixel)

cv2.waitKey(0)
