import cv2
import numpy as np

from StructDefine import *

'''
JPEG (Joint Photographic Experts Group)
Guetzli: 时间略长
WebP 
Icer Compression 
'''

def encodeImage(image, type = EncodeType.Origin):
    global g_nWidth
    global g_nHeight

    g_nHeight = image.shape[0]
    g_nWidth = image.shape[1]
    try:
        if (type == EncodeType.Origin):
            data = np.array(image.data)
            byteCount = data.shape[0] * data.shape[1] * data.shape[2]
        elif (type == EncodeType.JPEG):
            res, data = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            data = np.array(data)
            byteCount = data.shape[0]
        elif (type == EncodeType.WebP):
            res, data = cv2.imencode('.webp', image, [int(cv2.IMWRITE_WEBP_QUALITY), 95])
            data = np.array(data)
            byteCount = data.shape[0]
        elif (type == EncodeType.Segment):
            segImage = image
            for i in range((int)(g_nHeight / 3), (int)(g_nHeight * 2 / 3)):
                for j in range((int)(g_nWidth / 3), (int)(g_nWidth * 2 / 3)):
                    segImage[i][j][0] = 0
                    segImage[i][j][1] = 0
                    segImage[i][j][2] = 0
            res, data = cv2.imencode('.jpg', segImage, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            data = np.array(data)
            byteCount = data.shape[0]
        else:
            return False, None, 0
        print('encode', type, 'size (byte)', byteCount)
        return True, data, byteCount
    except Exception as e:
        print(e)
        return False, None, 0
    
def decodeImage(data, byteCount = 0, type = EncodeType.Origin):
    try:
        if (type == EncodeType.Origin):
            image = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = np.reshape(image, (g_nHeight, g_nWidth, 3))
        elif (type == EncodeType.JPEG):
            buffer = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        elif (type == EncodeType.Segment):
            buffer = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        elif (type == EncodeType.WebP):
            buffer = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        else:
            return False, None
        return True, image
    except Exception as e:
        print(e)
        return False, None
    
def encodeDecodeImages(image, eEncodeType = EncodeType.Origin):
    res, data, byteCount = encodeImage(image, eEncodeType)
    if res == False:
        print('error encode in', eEncodeType)
        return 0
    res, recoverImage = decodeImage(data, byteCount, eEncodeType)
    if (res == False):
        print('error decode in', eEncodeType)
        return 0
    cv2.imshow('{}'.format(eEncodeType), recoverImage)
    cv2.waitKey(1000)
    return byteCount

if __name__ == '__main__':
    typeNum = 4
    byteCount = [0] * typeNum 
    sImgName = '/home/channy/Documents/datasets/rgb_dataset/images/00001_lgd2.jpg'
    image = cv2.imread(sImgName)

    byteCount[0] = encodeDecodeImages(image, EncodeType.Origin)
    # byteCount[1] = encodeDecodeImages(image, EncodeType.JPEG)
    # byteCount[2] = encodeDecodeImages(image, EncodeType.Segment)
    byteCount[3] = encodeDecodeImages(image, EncodeType.WebP)

    for i, c in enumerate(byteCount):
        print(i, c / byteCount[0])
