import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def detect_sift(img):
	sift = cv2.SIFT_create()	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kp = sift.detect(gray, None)
	kp, des = sift.compute(gray, kp)
	nimg = cv2.drawKeypoints(img, kp, img)
	#cv2.imshow('feature', nimg)
	#cv2.waitKey()
	return kp, des

def match_sift(image1, image2, size = (480, 270)):
	img1 = cv2.resize(image1, size)
	img2 = cv2.resize(image2, size)
	kp1, des1 = detect_sift(img1)
	kp2, des2 = detect_sift(img2)
	
	bf = cv2.BFMatcher(crossCheck=True)
	matches = bf.match(des1, des2)
	res = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
	r = cv2.resize(res, size)
	cv2.imshow('feature', r)
	cv2.waitKey(10)

def depth_map():
	imgL = cv2.imread('IMG_0093.jpg',0)
	imgR = cv2.imread('IMG_0094.jpg',0)
	stereo = cv2.StereoBM_create(numDisparities=1024, blockSize=15)
	disparity = stereo.compute(imgL,imgR)
	plt.imshow(disparity,'gray')
	plt.show()

if __name__ == '__main__':
	path = 'D:/dataset/lab/parking/images'
	files = os.listdir(path)
	i = 0
	print(len(files))
	for file in files:
		if not os.path.isdir(file):
			if (i == 0):
				preimg = cv2.imread(path + '/' + file)
				i = i + 1
				continue
			img = cv2.imread(path + '/' + file)
			match_sift(preimg, img)
			preimg = img
			i = i + 1