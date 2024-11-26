import cv2
import json
import subprocess

from StructDefine import *

def getVideoFileSize(file_path):
    command = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=size',
        '-of', 'json', file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = json.loads(result.stdout.decode('utf-8'))
    return int(output['format']['size'])

    
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
            out_video = cv2.VideoWriter('tmp.mp4', cv2.VideoWriter_fourcc(*"mp4v"), fps, (g_nWidth, g_nHeight))
            while cap.isOpened():
                ret, segImage = cap.read()
                if ret:
                    for i in range((int)(g_nHeight / 3), (int)(g_nHeight * 2 / 3)):
                        for j in range((int)(g_nWidth / 3), (int)(g_nWidth * 2 / 3)):
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



def encodeDecodeVideos(sVideoName, eEncodeType = EncodeType.Origin):
    res, byteCount = encodeVideo(sVideoName, eEncodeType)
    return byteCount


if __name__ == '__main__':
    count = [0, 0, 0]

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