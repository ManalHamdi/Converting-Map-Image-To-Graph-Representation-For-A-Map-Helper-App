import cv2
import numpy as np 
import matplotlib.pyplot as plt

def IsIndexValid(i, j, rows, columns):
	if (i >= 0 and i <= rows - 1 and j >= 0 and j <= columns - 1):
		return True
	else:
		return False

def IsDoubleRoadPixel(image, i, j, rw):
	rows = image.shape[0]
	col = image.shape[1]
	r = False
	c = False
	if (IsIndexValid(i, j-rw, rows, col) and (image[i, j - rw] == [255, 255, 255]).all()):
		r = True
	elif(IsIndexValid(i, j+rw, rows, col) and (image[i, j+rw] == [255, 255, 255]).all()):
		r = True
	if (r == False):
		return False
	if (IsIndexValid(i-rw, j, rows, col) and (image[i-rw, j] == [255, 255, 255]).all()):
		c = True
		return True
	elif (IsIndexValid(i+rw, j, rows, col) and (image[i+rw, j] == [255, 255, 255]).all()):
		c = True
		return True
	return False

def CountForegroundPixels(image):
	count = 0
	for i in range (0, image.shape[0]):
		for j in range (0, image.shape[1]):
			if ((image[i, j] == [255, 255, 255]).all()):
				count += 1
	return count
def PlotAndSave(x, y, x_label, y_label, saving_name):
	plt.plot(x, y, 'ro')
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.savefig(saving_name)
	plt.show() 
	

def ParallelPatternTracing(image, max_rw):
	count_array = np.zeros(max_rw + 1)
	count = CountForegroundPixels(image)
	new_count = count
	rows = image.shape[0]
	col = image.shape[1]
	for rw in range(1, max_rw + 1):
		new_count = count
		for i in range(0, rows):
			for j in range(0, col):
				if ((image[i, j] == [255, 255, 255]).all() and IsDoubleRoadPixel(image, i, j, rw) == False):
					new_count -= 1
		count_array[rw] = new_count / count
		print(rw, new_count / count)
	x = np.arange(rw + 1)
	PlotAndSave(x, count_array, "Test L1 Double P", "Ratio", "PlotTest/PlotTest L1 Double P.png")

	

def ExtractRoadPixels(original_image_name, bgr, thresh):
	minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
	maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh]) 
	original_image = cv2.imread(original_image_name)
	mask_b = cv2.inRange(original_image, minBGR, maxBGR)
	image = cv2.bitwise_and(original_image, original_image, mask = mask_b)
	return image


bgr = [235, 235, 235]
thresh = 20

image = ExtractRoadPixels("PlotTest/L1 Double P.png", bgr, thresh)
ParallelPatternTracing(image, 15)









