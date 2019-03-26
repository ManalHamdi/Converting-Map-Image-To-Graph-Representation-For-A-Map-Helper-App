import cv2
import numpy as np

def IsIndexValid(i, j, rows, columns):
	if (i >= 0 and i <= rows - 1 and j >= 0 and j <= columns - 1):
		return True
	else:
		return False
def Structuring(original_image, i, j):
	if (original_image[i-1, j-1] == 0 and original_image[i-1, j] == 0 and original_image[i-1, j+1] == 0 and original_image[i+1, j-1] == 255 and original_image[i+1, j] == 255 and original_image[i+1, j+1] == 255):
		return False
	if (original_image[i-1, j-1] == 255 and original_image[i, j-1] == 255 and original_image[i+1, j-1] == 255 and original_image[i-1, j+1] == 0 and original_image[i, j+1] == 0 and original_image[i+1, j+1] == 0):
		return False
	if (original_image[i-1, j-1] == 0 and original_image[i, j-1] == 0 and original_image[i+1, j-1] == 0 and original_image[i-1, j+1] == 255 and original_image[i, j+1] == 255 and original_image[i+1, j+1] == 255):
		return False
	if (original_image[i-1, j-1] == 255 and original_image[i-1, j] == 255 and original_image[i-1, j+1] == 255 and original_image[i+1, j-1] == 0 and original_image[i+1, j] == 0 and original_image[i+1, j+1] == 0):
		return False
	
	if (original_image[i-1, j] == 0 and original_image[i-1, j+1] == 0 and original_image[i, j+1] == 0 and original_image[i, j-1] == 255 and original_image[i+1, j] == 255):
		return False
	if (original_image[i-1, j] == 255 and original_image[i, j-1] == 255 and original_image[i, j+1] == 0 and original_image[i+1, j+1] == 0 and original_image[i+1, j] == 0):
		return False
	if (original_image[i-1,j] == 255 and original_image[i, j+1] == 255 and original_image[i, j-1] == 0 and original_image[i+1, j-1] == 0 and original_image[i+1, j] == 0):
		return False
	if (original_image[i-1, j-1] == 0 and original_image[i-1, j] == 0 and original_image[i, j-1] == 0 and original_image[i, j+1] == 255 and original_image[i+1, j] == 255):
		return False

	return True


def Thinning(original_image):
	result = original_image.copy()

	rows = original_image.shape[0]
	columns = original_image.shape[1]

	for i in range (1, rows - 1):
			for j in range(1, columns - 1):
				if (original_image[i, j] == 255):
					if (Structuring(original_image, i, j) == False): #if the image pixels match the structuring pixels
						result[i,j] = 0
	return result
def Erosion(original_image, number_iterations):
	rows = original_image.shape[0]
	columns = original_image.shape[1]
	
	result = original_image.copy()

	for k in range(1, number_iterations + 1): 
		for i in range (0, rows):
			for j in range(0, columns):
				if (original_image[i, j] == 255):
					flag = False
					for a in range(-1,2):
						for b in range(-1,2):

							if (IsIndexValid(i+a, j+b, rows, columns) and original_image[i+a, j+b] == 0):
								flag = True
								break
					if (flag == True):
						result[i,j] = 0
		if (k != number_iterations):
			original_image = result.copy()
	return result

def Dilation(original_image, number_iterations):
	result = original_image.copy()	
	
	rows = original_image.shape[0]
	columns = original_image.shape[1]	
	
	for k in range(1, number_iterations + 1): 
		for i in range (0, rows):
			for j in range(0, columns):
				if ((original_image[i, j] == [0,0,0]).all()):
					flag = False
					for a in range(-1,2):
						for b in range(-1,2):
							if (IsIndexValid(i+a, j+b, rows, columns) and (original_image[i+a, j+b] == [255, 255, 255]).all()):
								flag = True
								break
					if (flag == True): 
						result[i,j] = [255, 255, 255]
		if (k != number_iterations): 
			original_image = result.copy()
	
	return result

def DisplaySaveImage(image, save_name, display_name):
	cv2.imwrite(save_name, image)
	#cv2.imshow(display_name, image)
	
def ExtractRoadPixels(original_image_name, bgr, thresh):
	minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
	maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh]) 
	original_image = cv2.imread(original_image_name)
	mask_b = cv2.inRange(original_image, minBGR, maxBGR)
	image = cv2.bitwise_and(original_image, original_image, mask = mask_b)
	return image

bgr = [253, 253, 253]
thresh = 2
image = ExtractRoadPixels("doublelineAUI.png", bgr, thresh)
d = Dilation(image, 3)
cv2.imwrite("doublelineAUI Dilated.png", d)

# bwimage = image[:,:,1]

#print(bwimage.shape)
#print(bwimage)

# bwimage[:,6] = [255]*10
# bwimage[:,2] = [255]*10
# bwimage[2,0:3] = [255]*3
# bwimage[6,0:3] = [255]*3

# e1 = Erosion(bwimage, 1)
# e2 = Erosion(bwimage, 2)
# t1 = Thinning(bwimage)
# t2 = Thinning(e1)
# t3 = Thinning(e2)

# print(e1)
# print(e2)
# print(t1)
# print(t2)
# print(t3)

#cv2.imwrite("TjunctionThinningWIthoutErosion.png", t)
#print(bwimage)



