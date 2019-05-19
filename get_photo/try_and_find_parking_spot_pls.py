import cv2
from math import sqrt


# redundant, no use anymore, keeping it because well, better safe than sorry
def write_to_file(index, matrix):
	filename = 'matrix' + str(index) + '.txt'
	f = open(filename, 'w')
	height, width = matrix.shape[:2]
	print("Height = ", height, " Width = ", width)
	for i in range(width):
		for j in range(height):
			#print("i = ", i, " j = ", j)
			f.write(str(matrix[j][i]))
		f.write('\n')


def euclidian_distance(x1, y1,x2,y2):
	return sqrt((x1-x2)**2 + (y1-y2)**2)

# returns true if two rectangles overlap
def overlaps(x1,y1,w1,h1,x2,y2,w2,h2):
	center1 = (x1 + w1/2,y1 + h1/2)
	center2 = (x2 + w2/2, y2 + h2/2)
	distance = euclidian_distance(center1[0],center1[1],center2[0],center2[1])
	if distance <= w1/2 + w2/2:
		return True
	else:
		return False


def find_parking_place(image):
	height, width = image.shape[:2]
	threshold = 237
	maxPair = (0, 0, 0, 0) # p1.x, p1.y, p2.x, p2.y
	maxDist = 0
	oldMaxDist = 0
	for i in range(width):
		if image[int(height/2)][i] == 255:
			for j in range(i, width):
				if image[int(height/2)][j] == 255:
					if euclidian_distance(i, int(height/2),j,int(height/2)) > threshold:
						maxPair = (i, int(height/2),j, int(height/2))
						break
	return maxPair

def main():
	cap = cv2.VideoCapture(0)
	car_cascade = cv2.CascadeClassifier('cars.xml')
	img_count = 5
	w,h = 40, 40
	w_car, h_car = 100,100
	while 1:
		ret, img = cap.read()
		grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		grayscale_slice = grayscale[0:480, 0:320]
		cars = car_cascade.detectMultiScale(grayscale,1.1,3)
		circles = cv2.HoughCircles(grayscale_slice, cv2.HOUGH_GRADIENT, 1,20,
			param1 = 50, param2 = 30, minRadius = 10, maxRadius = 30)
		if circles is not None:
			for (x_car,y_car,_,_),i in zip(cars,circles[0,:]):
				cv2.rectangle(img, (x_car,y_car),(x_car+w_car,y_car+h_car),(0,255,0),2) # green --> cars
				cv2.rectangle(img, (int(i[0]) - int(w/2), int(i[1])-int(h/2)), (int(i[0]) + int(w/2), int(i[1]) + int(h/2)),(0,0,255),2) # red --> circle
				if overlaps(x_car,y_car,w,h,int(i[0]),int(i[1]),w_car,h_car) == True:
					print("Overlap")
		else:
			for (x,y,w,h) in cars:
				cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)
		cv2.imshow('Image',img)
		# escape key
		k = cv2.waitKey(30) & 0xff

		if k == 27:
			break

if __name__ == '__main__':
	main()
