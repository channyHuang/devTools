# -*- coding: utf-8 -*-
import cv2
import os
import argparse

# resize图像集
def resizeImgFolder(inPath, outPath, size = (640, 480)):
    files = os.listdir(inPath)
    for filename in files:
        if not os.path.isdir(filename):
            img = cv2.imread(inPath + '/' + filename)
            nimg = cv2.resize(img, size)
            cv2.imwrite(outPath + '/' + filename, nimg)

# 图像后缀转换
def changeImageExt(inPath, outExt = 'png'):
    name = inPath.split('.')[0]
    img = cv2.imread(inPath)
    cv2.imwrite(name + '.' + outExt, img)

# 从图像集中选取子图像集
def selectImgSequence(inPath, outPath, gap = 30):
	files = os.listdir(inPath)
	i = 0
	j = 0
	for file in files:
		if not os.path.isdir(file):
			if (i % gap == 0):
				img = cv2.imread(inPath + '/' + file)
				cv2.imwrite(outPath + '/' + file, img)
				j = j + 1
			i = i + 1
                  
# 循环读取HEIC格式照片，写入JPG
def recyle_convert(org_path, dst_path):
    from PIL import Image
    import pillow_heif
    import whatimage

    # 判断是不是目录
    if os.path.isdir(org_path):
        file_list = os.listdir(org_path)
        for idx, file in enumerate(file_list):
            sub_path = os.path.join(org_path, file)
            recyle_convert(sub_path, dst_path)
    # 判断是不是文件
    elif os.path.isfile(org_path):
        with open(org_path, 'rb') as f:
            file_data = f.read()
            try:
                # 判断照片格式
                fmt = whatimage.identify_image(file_data)
                if fmt in ['heic']:
                    # 读取图片
                    heif_file = pillow_heif.read_heif(org_path)
                    image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
                    # 将要存储的路径及名称
                    path, filename = os.path.split(org_path)
                    name, ext = os.path.splitext(filename)
                    file_path = os.path.join(dst_path, '%s.jpg' % name)
                    image.save(file_path, "JPEG")
            except:
                print('except')
    else:
        print(org_path + 'is error format!')

#############################              

# mov视频分解成图像集
def mov2imgSequence(sVideoName = 'D:/dataset/lab/IMG_0080.MOV', outPath = "./", gap = 0):
    raw = cv2.VideoCapture(sVideoName, cv2.CAP_FFMPEG)
    if (raw.isOpened()):
        print('open success')
    i = 0
    while (True):
        ret, frame = raw.read()
        if (ret == False):
            break
        if ((gap == 0) or (gap > 0 and i % gap == 0)):
            cv2.imwrite(outPath + ('%05d' % i) + '.jpg', frame)
        i = i + 1

# mov视频转换成mp4
def mov2mp4(sVideoName, sOutVideo = 'out.mp4', size = (1920, 1080), cap_fps = 30):
    out = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(sOutVideo, out, cap_fps, size)
    raw = cv2.VideoCapture(sVideoName)
    while (True):
        ret, frame = raw.read()
        if (ret == False):
            break
        video.write(frame)
    video.release()

def mov2gif():
    from moviepy.editor import *
    
	content = VideoFileClip('E:/recon-result/lab_back_res/IMG_0225.MOV')
	c = content.fx(vfx.resize, width = 960)
	c.write_gif('E:/recon-result/res.gif', fps = 120)

# 图像序列转换成mp4
def imageSeq2mp4(inPath, sOutVideo = 'out.mp4', size = (1920, 1080), cap_fps = 30):
    out = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(sOutVideo, out, cap_fps, size)
    files = os.listdir(inPath)
    for filename in files:
        img = cv2.imread(inPath + '/' + filename)
        video.write(img)
    video.release()

# 图像序列转换成gif
def imageSeq2gif():
    import imageio

    with imageio.get_writer(uri='E:/recon-result/lab_tmp.gif', mode='I', fps=20) as writer:
    	for i in range(200):
			n = "%05d" % (i + 1)
			#if (i % 1 == 0):
			img = imageio.imread(f'E:/recon-result/lab/{i}.jpg')
			img = cv2.resize(img, (960, 540)) 
			writer.append_data(img)
		for i in range(200, -1, -1):
			n = "%05d" % (i + 1)
			#if (i % 1 == 0):
			img = imageio.imread(f'E:/recon-result/lab/{i}.jpg')
			img = cv2.resize(img, (960, 540)) 
			writer.append_data(img)

#############################

def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

def sharpness(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	return fm

def imgSharpness(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	return fm

def selectSharpness(path):
    files = os.listdir(path)
    for filename in files:
        sharpVal = sharpness(path + '/' + filename)
        if (sharpVal < 100):
            frame = cv2.imread(path + '/' + filename)
            cv2.waitKey(1000)

# 根据sharpness选取关键帧
def selectKeyframe(sVideoName, sOutPath, nGap = 15):
	raw = cv2.VideoCapture(sVideoName, cv2.CAP_FFMPEG)
	if (raw.isOpened()):
		print('open success')
	nLastIdx = -1
	nMaxSharpness = -1
	nMaxIdx = -1
	nCurIdx = -1
	while (True):
		ret, frame = raw.read()
		if (ret == False):
			break
		nCurIdx = nCurIdx + 1
		sharpVal = imgSharpness(frame)
		if (nLastIdx == -1):
			nLastIdx = nCurIdx
			cv2.imwrite(sOutPath + ('%05d' % nCurIdx) + '.jpg', frame)
			nMaxSharpness = -1
		if (nCurIdx - nLastIdx < nGap):
			continue
		if (sharpVal >= nMaxSharpness):
			nMaxSharpness = sharpVal
			maxFrame = frame
			nMaxIdx = nCurIdx
		if (nCurIdx - nLastIdx >= nGap * 2):
			if (nMaxIdx > 0):
				nLastIdx = nMaxIdx
				cv2.imwrite(sOutPath + ('%05d' % nMaxIdx) + '.jpg', maxFrame)
				nMaxSharpness = -1
				nMaxIdx = -1



def parse_args():
	parser = argparse.ArgumentParser(description="...")
	parser.add_argument("--path", default="", help="...")
	parser.add_argument("--file", default="", help="...")
	parser.add_argument("--inPath", default="", help="...")
	#parser.add_argument("--outPath", default="", help="...")
	args = parser.parse_args()
	return args

if __name__ == "__main__":
    args = parse_args()
    selectKeyframe('E:/parking.mov', 'D:/dataset/lab/parking/images/', 15)