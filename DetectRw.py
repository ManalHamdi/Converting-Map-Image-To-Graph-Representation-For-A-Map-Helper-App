import cv2
import numpy as np 
import matplotlib.pyplot as plt

def ExtractRoadPixels(original_image_name, bgr, thresh):
	minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
	maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh]) 
	original_image = cv2.imread(original_image_name)
	
	mask_b = cv2.inRange(original_image, minBGR, maxBGR)
	image = cv2.bitwise_and(original_image, original_image, mask = mask_b)
	return mask_b

def DetectPotentialRw(small_image):
	r = small_image.shape[0]
	c = small_image.shape[1]
	
	#Count number of changes
	#Horizontally
	mx_h = 0 
	avg_h = 0
	count = 0
	for i in range(0, r, int(r / 4)):
		chg = 0
		count += 1 
		for j in range(1, c):
			if (small_image[i, j] != small_image[i, j - 1]):
				chg += 1
		print("H for i = ", i, "chg", chg)
		avg_h += chg
		if (chg > mx_h):
			mx_h = chg
			index_h = i
	avg_h /= count

	#Vertically
	count = 0
	avg_v = 0
	mx_v = 0
	for j in range(0, c, int(c / 4)):
		chg = 0
		count += 1 
		for i in range(1, r):
			if (small_image[i, j] != small_image[i - 1, j]):
				chg += 1
		print("V for j = ", j, "chg", chg)
		avg_v += chg
		if (chg > mx_v):
			mx_v = chg
			index_v = j
	avg_v /= count
	print("V", avg_v, "H", avg_h) 
	if (avg_h >= avg_v): #road is oriented horizontally
		if (mx_h > 2): #road is double Detect this pattern 0* 1* 0* 1* 0*
			lw = 0
			in_seq = 0 #0 means never saw 255
			mx_lw = 0
			rw = 0
			
			for j in range(0, c): #Get Line Width
				if (in_seq == 0 and small_image[index_h, j] == 255):
					in_seq = 1 #1 means in first white sequence 
					lw += 1
				elif (in_seq == 1 and small_image[index_h, j] == 255):
					lw += 1
				elif (in_seq == 1 and small_image[index_h, j] == 0):
					rw += 1
					in_seq = 2 #2 means in between lines
					if (lw > mx_lw):
						mx_lw = lw
						lw = 0
				elif (in_seq == 2 and small_image[index_h, j] == 0):
					rw += 1
				
				elif (in_seq == 2 and small_image[index_h, j] == 255):
					lw = 1
					in_seq = 3
				elif (in_seq == 3 and small_image[index_h, j] == 255):
					lw += 1
				elif (in_seq == 3 and small_image[index_h, j] == 0):
					if (lw > mx_lw):
						mx_lw = lw
						lw = 0
					in_seq = 4
					break
			#print("H Double lw", lw, "Rw", rw)
			return [lw, rw]
		else: #Single, get lw
			lw = 0
			for j in range(0, c):
				if (small_image[index_h, j] == 255):
					lw += 1
			#print("Single lw" , lw)
			return [lw, 0]
	else: #road is oriented horizontally
		if (mx_v > 2): #road is double Detect this pattern 0* 1* 0* 1* 0*
			lw = 0
			in_seq = 0 #0 means never saw 255
			mx_lw = 0
			rw = 0
			
			for i in range(0, r): #Get Line Width
				if (in_seq == 0 and small_image[i, index_v] == 255):
					in_seq = 1 #1 means in first white sequence 
					lw += 1
				elif (in_seq == 1 and small_image[i, index_v] == 255):
					lw += 1
				elif (in_seq == 1 and small_image[i, index_v] == 0):
					rw += 1
					in_seq = 2 #2 means in between lines
					if (lw > mx_lw):
						mx_lw = lw
						lw = 0
				elif (in_seq == 2 and small_image[i, index_v] == 0):
					rw += 1
				
				elif (in_seq == 2 and small_image[i, index_v] == 255):
					lw = 1
					in_seq = 3
				elif (in_seq == 3 and small_image[i, index_v] == 255):
					lw += 1
				elif (in_seq == 3 and small_image[i, index_v] == 0):
					if (lw > mx_lw):
						mx_lw = lw
						lw = 0
					in_seq = 4
					break
			#print("V Double lw", lw, "Rw", rw)
			return [lw, rw]

		else: #Single, get lw
			lw = 0
			for i in range(0, r):
				if (small_image[i, index_v] == 255):
					lw += 1
			#print("Single lw" , lw)
			return [lw, 0]




bgr = [235, 235, 235]
thresh = 20

image = ExtractRoadPixels("Map 3.png", bgr, thresh)
pair = DetectPotentialRw(image)
lw = pair[0]
rw = pair[1]
if (rw == 0):
	print("Single with lw", lw)

else:
	print("Double with lw", lw, "Rw", rw)






