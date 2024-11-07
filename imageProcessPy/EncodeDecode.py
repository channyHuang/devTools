import numpy as np
import cv2
from enum import Enum
import subprocess
import json

class EncodeType(Enum):
    Origin = 1
    JPEG = 2
    Segment = 3
    H265 = 4

nHeight = 1080
nWidth = 1920

def getVideoFileSize(file_path):
    command = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=size',
        '-of', 'json', file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = json.loads(result.stdout.decode('utf-8'))
    return int(output['format']['size'])

def encodeImage(image, type = EncodeType.Origin):
    nHeight = image.shape[0]
    nWidth = image.shape[1]
    try:
        if (type == EncodeType.Origin):
            data = np.array(image.data)
            byteCount = data.shape[0] * data.shape[1] * data.shape[2]
        elif (type == EncodeType.JPEG):
            res, data = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            data = np.array(data)
            byteCount = data.shape[0]
        elif (type == EncodeType.Segment):
            segImage = image
            for i in range((int)(nHeight / 3), (int)(nHeight * 2 / 3)):
                for j in range((int)(nWidth / 3), (int)(nWidth * 2 / 3)):
                    segImage[i][j][0] = 0
                    segImage[i][j][1] = 0
                    segImage[i][j][2] = 0
            res, data = cv2.imencode('.jpg', segImage, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            data = np.array(data)
            byteCount = data.shape[0]
        else:
            return False, None
        print('encode', type, 'size (byte)', byteCount)
        return True, data, byteCount
    except Exception as e:
        print(e)
        return False, None, 0
    
def decodeImage(data, byteCount = 0, type = EncodeType.Origin):
    try:
        if (type == EncodeType.Origin):
            image = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = np.reshape(image, (nHeight, nWidth, 3))
        elif (type == EncodeType.JPEG):
            buffer = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        elif (type == EncodeType.Segment):
            buffer = np.frombuffer(data, dtype = np.ubyte, count = byteCount)
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        else:
            return False, None
        return True, image
    except Exception as e:
        print(e)
        return False, None
    
def encodeVideo(sVideoName, type = EncodeType.Origin):
    sOutVideoName = 'HG_{}.mp4'.format(type)
    byteCount = 0
    try:
        if (type == EncodeType.Origin):
            byteCount = getVideoFileSize(sVideoName)
        elif (type == EncodeType.H265):
            command = ('ffmpeg', '-ss', '10', '-i', sVideoName, '-vcodec', 'libx265', '-crf', '23', sOutVideoName)
            subprocess.call(command)
            byteCount = getVideoFileSize(sOutVideoName)
        elif (type == EncodeType.Segment):
            cap = cv2.VideoCapture(sVideoName)
            fps = cap.get(cv2.CAP_PROP_FPS)
            out_video = cv2.VideoWriter('tmp.mp4', cv2.VideoWriter_fourcc(*"mp4v"), fps, (nWidth, nHeight))
            while cap.isOpened():
                ret, segImage = cap.read()
                if ret:
                    for i in range((int)(nHeight / 3), (int)(nHeight * 2 / 3)):
                        for j in range((int)(nWidth / 3), (int)(nWidth * 2 / 3)):
                            segImage[i][j][0] = 0
                            segImage[i][j][1] = 0
                            segImage[i][j][2] = 0
                    out_video.write(segImage)
                else:
                    break
            out_video.release()
            command = ('ffmpeg', '-ss', '10', '-i', 'tmp.mp4', '-vcodec', 'libx265', '-crf', '23', sOutVideoName)
            subprocess.call(command)
            byteCount = getVideoFileSize(sOutVideoName)
        else:
            return False, byteCount
        print('encode', type, 'size (byte)', byteCount)
        return True, byteCount
    except Exception as e:
        print(e)
        return False, byteCount

def encodeDecodeImages(image, eEncodeType = EncodeType.Origin):
    res, data, byteCount = encodeImage(image, eEncodeType)
    if res == False:
        print('error encode in', eEncodeType)
        return
    res, recoverImage = decodeImage(data, byteCount, eEncodeType)
    if (res == False):
        print('error decode in', eEncodeType)
        return
    cv2.imshow('{}'.format(eEncodeType), recoverImage)
    cv2.waitKey(1000)
    return byteCount

def encodeDecodeVideos(sVideoName, eEncodeType = EncodeType.Origin):
    res, byteCount = encodeVideo(sVideoName, eEncodeType)
    return byteCount


if __name__ == '__main__':
    count = [0, 0, 0]
    if (1):
        sImgName = '/home/channy/Documents/datasets/rgb_dataset/images/00001_lgd2.jpg'
        image = cv2.imread(sImgName)

        count[0] = encodeDecodeImages(image, EncodeType.Origin)
        count[1] = encodeDecodeImages(image, EncodeType.JPEG)
        count[2] = encodeDecodeImages(image, EncodeType.Segment)

        for i, c in enumerate(count):
            print(i, c / count[0])
        # 0 1.0
        # 1 0.09133182227366256
        # 2 0.08265560699588477


    if (0):
        sVideoName = '/home/channy/Documents/datasets/1920_test.mp4'
        count[0] = encodeDecodeVideos(sVideoName, EncodeType.Origin)
        count[1] = encodeDecodeVideos(sVideoName, EncodeType.H265)
        count[2] = encodeDecodeVideos(sVideoName, EncodeType.Segment)
        for i, c in enumerate(count):
            print(i, c / count[0])
        # 0 1.0
        # 1 0.5403287443267949
        # 2 0.45410097382522907