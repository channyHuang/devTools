import cv2

cap = cv2.VideoCapture('/home/channy/Documents/datasets/1120数据/DJI_202411201623_055/DJI_20241120163406_0002_W.MP4')
nframe = 0
while (cap.isOpened()):
    res, frame = cap.read()
    if res is None or res == False:
        break
    nframe += 1
    if nframe % 100 == 0:
        cv2.imwrite('./cut/' + str(nframe) + '.jpg', frame)
