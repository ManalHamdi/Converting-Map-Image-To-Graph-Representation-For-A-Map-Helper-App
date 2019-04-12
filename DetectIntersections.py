import cv2
import numpy as np 
import math

def ExtractRoadPixels(original_image_name, bgr, thresh):
	minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
	maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh]) 
	original_image = cv2.imread(original_image_name)
	mask_b = cv2.inRange(original_image, minBGR, maxBGR)
	image = cv2.bitwise_and(original_image, original_image, mask = mask_b)
	return image

def CheckSegmentFrame(image, from_i, to_i, from_j, to_j):
	r = image.shape[0]
	c = image.shape[1]
	point_intersection = set()
	for i in range(from_i, to_i + 1):
		for j in range(from_j, to_j + 1):
			if (IsIndexValid(i, j, r, c) and (image[i, j] == [255, 255, 255]).all()):
				point_intersection.add((i, j))
	return point_intersection

def IsIndexValid(i, j, rows, columns):
	if (i >= 0 and i <= rows - 1 and j >= 0 and j <= columns - 1):
		return True
	else:
		return False

def DetectIntersections(image, size_frame):
	r = image.shape[0]
	c = image.shape[1]

	result = image.copy()
	detected_intersection = set()
	for i in range(0, r):
		for j in range(0, c):
			if ((i == 0 or i == r-1 or j == 0 or j == c-1) and  (image[i, j] == [255, 255, 255]).all()):
				detected_intersection.add((i,j))
				result[i, j] = [36, 36, 144]
	
			if ((image[i, j] == [255, 255, 255]).all()):
				upper_h = CheckSegmentFrame(image, i - size_frame, i - size_frame, j - size_frame, j + size_frame) #upper h 
				lower_h = CheckSegmentFrame(image, i + size_frame, i + size_frame, j - size_frame, j + size_frame) #lower h
				
				left_v = CheckSegmentFrame(image, i - size_frame, i + size_frame, j - size_frame, j - size_frame) #left v
				right_v = CheckSegmentFrame(image, i - size_frame, i + size_frame, j + size_frame, j + size_frame) #right v

				point_intersection = upper_h | lower_h | left_v | right_v
				if (len(point_intersection) > 2):
					detected_intersection.add((i,j))
					result[i, j] = [36, 36, 144]
					#print("For i =", i, "j =", j, point_intersection)
				if (len(point_intersection) == 2): #Check if slope is the same to know whether it is the same line
					l = list(point_intersection)
					
					slope1 = math.inf
					slope2 = math.inf

					if ((i - l[0][0]) != 0):
						slope1 = (j - l[0][1]) / (i - l[0][0])
					if ((i - l[1][0]) != 0):
						slope2 = (j - l[1][1]) / (i - l[1][0])					
					if (slope1 != slope2):
						#print("For i =", i, "j =", j, point_intersection)
						detected_intersection.add((i,j))
						result[i, j] = [36, 36, 144]
	cv2.imwrite('DetectIntersectionsPictures/Map 1 Colored 1.png', result)
	return sorted(detected_intersection)

def find(parent, point):
    if (point != parent[point]):
        parent[point] = find(parent, parent[point])
    return parent[point]

def union(parent, point1, point2):
    p1, p2 = find(parent, point1), find(parent, point2)
    if (p1 < p2):
        parent[p2] = p1

def connected(parent, point1, point2):
    return find(parent, point1) == find(parent, point2)

def IsNeighbour(point1, point2):
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (i == 0 and j == 0):
				continue
			if (point1[0] == point2[0] + i and point1[1] == point2[1] + j):
				return True
	return False
def GroupIntersections(detected_intersection):
	parent = dict()		
	for point in detected_intersection:
		parent[point] = point

	for point1 in detected_intersection:
		for point2 in detected_intersection:
			if (point1 == point2):
				continue
			#Are they in the same set
			if (connected(parent, point1, point2)):
				continue
			#Are they neighbours
			if (IsNeighbour(point1, point2)):
				union(parent, point1, point2)
	return parent

# def Fun(origin, image, parent, graph, detected_intersection):
# 	x = origin[0]
# 	y = origin[1]

# 	for a in range(-1, 2):
# 		for b in range(-1, 2):
# 			if (a == 0 and b == 0):
# 				continue
# 			if ((x + a, y + b) in detected_intersection and connected(parent, origin, (x+a, y+b)) == False):
# 				graph[find(origin)].append(find(x+a, y+b))
# 				graph[find(x+a, y+b)].append(find(origin))
				

# 			elif ((image[x + a, y + b] == [255, 255, 255]).all()):
# 				Fun((x + a, y + b), image, parent, graph, detected_intersection)

def belongs(item, itemset):
	for entry in itemset:
		if entry == item:
			return True
	return False

def dfs(pixel, image, graph, visited, detected_intersection, parent):
	dx =  [1, 1, 1, -1, -1, -1, 0, 0]
	dy =  [-1, 1, 0, 1, 0, -1, 1, -1]

	x, y = pixel
	
	#print(pixel)
	
	visited[pixel] = True

	for i in range(len(dx)):
		nx = x + dx[i]
		ny = y + dy[i]
		if not IsIndexValid(nx, ny, image.shape[0], image.shape[1]):
			continue

		if (belongs((nx, ny), detected_intersection)):
			if visited[(nx, ny)]:
				continue
			#print('we belong to the sam set yaaay {} {}'.format(pixel, (nx, ny)))
			dfs((nx, ny), image, graph, visited, detected_intersection, parent)
		else:
			while(image[nx, ny] == [255, 255, 255]).all():
				nx += dx[i]
				ny += dy[i]

				if (belongs((nx, ny), detected_intersection)):
					if visited[(nx, ny)]:
						break

					cost = ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
					u = find(parent, (x, y))
					v = find(parent, (nx, ny))

				#	print('going to {} from {}'.format(v, u))

					graph[u].append((v, cost))  
					graph[v].append((u, cost))
					dfs((nx, ny), image, graph, visited, detected_intersection, parent)
					# add edge between the parent (x, y) and parent of (nx, ny)

					break

	
def DFS(point, image, graph, visited, detected_intersection, parent):
	''' 123
		405
		678

		


	'''
	dx =  [1, 1, 1, -1, -1, -1, 0]
	dy =  [-1, 1, 0, 1, 0, -1, 0]

	stack = [(point, 6)]
	while(len(stack) > 0):
		top = stack.pop()
		flag = False
		
		for ele in detected_intersection:
			if ele == top:
				flag = True
				break

		if (flag and visited[top]):
			continue

		if (flag):
			visited[top] = True

		if ((flag) and (connected(parent, top, point) == False)):
			point_par = find(parent, point)
			top_par = find(parent, top)
			graph[point_par].append([top_par, 1])
			graph[top_par].append([point_par, 1])
		else:
			for a in range(-1, 2):
				for b in range(-1, 2):
					if (a == 0 and b == 0):
						continue
					if ((image[top[0] + a, top[1] + b] == [255, 255, 255]).all()):
						stack.append((top[0] + a, top[1] + b))

def DetectEdges(image, detected_intersection, parent):
	graph = dict()
	visited = dict()
	for det_inter in detected_intersection:
		graph[find(parent, det_inter)] = []
		visited[det_inter] = False

	for det_inter in detected_intersection:
		if (visited[det_inter]):
			continue
		# changed to dfs rather than DFS
		dfs(det_inter, image, graph, visited, detected_intersection, parent)
	
	for key, value in graph.items():
		print('{}: {}'.format(key, value))

bgr = [235, 235, 235]
thresh = 20

image = ExtractRoadPixels("DetectIntersectionsPictures/Map 1.png", bgr, thresh)
detected_intersection = DetectIntersections(image, 1) #returns a set

parent = GroupIntersections(list(detected_intersection))

group_indentity = sorted(set(parent.values()))
print(len(group_indentity))
DetectEdges(image, detected_intersection, parent)
