import cv2
from math import sqrt
from math import pow

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
	return sqrt((x1-x2)**2 - (y1-y2)**2)

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
	img_count = 5
	while 1:
		ret, img = cap.read()
		grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gauss_grayscale_img = cv2.GaussianBlur(src=grayscale_img, ksize=(5, 5), sigmaX=0)
		edges_img = cv2.Canny(image=gauss_grayscale_img, threshold1=50, threshold2=150, apertureSize=3)
		sliced_edges_img = edges_img[240:480, 0:640]
		pair = find_parking_place(sliced_edges_img)
		try:
			cv2.line(sliced_edges_img,(pair[0],pair[1]),(pair[2],pair[3]),(255,255,255),3)
		except:
			pass
		# print("p1.x =  ", pair[0], ' p1.y = ', pair[1], ' p2.x = ', pair[2], ' p2.y = ', pair[3])
		cv2.imshow('cacat', sliced_edges_img)
		k = cv2.waitKey(30) & 0xff

		if k == 27:
			break

if __name__ == '__main__':
	main()
