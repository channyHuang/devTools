import cv2
import base64
import numpy as np

# video
def getVideoDuration(sVideoName):
    cap = cv2.VideoCapture(sVideoName)    
    nFps, nNumFrame, fDuration = 0, 0, -1
    if cap.isOpened():
        nFps = cap.get(cv2.CAP_PROP_FPS)
        nNumFrame =cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fDuration = nNumFrame / nFps

    sFileName =  os.path.split(sVideoName)[-1]
    return (sFileName, fDuration, nFps, nNumFrame)

def splitDirFiles(sDir, nBatchSize):
    vFileNames = os.listdir(sDir)
    nNumFile = len(vFileList)

    vSplitFiles = [[] for _ in range(nBatchSize)]
    vFileSize = [0 for _ in range(nBatchSize)] 

    vFileSortBySize = [] 
    for sFileName in vFileNames:
        sFileAbsPath = os.path.join(sDir, sFileName)
        fFileSize = os.path.getsize(sFileAbsPath)
        vFileSortBySize.append((sFileAbsPath, fFileSize))
    
    for (sFileAbsPath, fFileSize) in vFileSortBySize:
        idx = vFileSize.index(min(vFileSize))
        vFileSize[idx] += fFileSize
        vSplitFiles[idx].append(sFileAbsPath)

    return vSplitFiles

def getAllVideoDuration(sVideoDir):
    videos_info =  {}
    vVideoList = split_dataset(videos_dir, 1)[0]
    for sVideoName in vVideoList:
        (sFileName, fDuration, nFps, nNumFrame) = getVideoDuration(sVideoName)
        dVideoInfo[sFileName] = [sFileName, fDuration, nFps, nNumFrame]
    return dVideoInfo

# image
def encode_image(image):
    try:
        result, imgencode = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

        data = np.array(imgencode)
        stringData = data.tostring()
        stringData = base64.b64encode(stringData)

        stringData = stringData.decode()
        return True, stringData
    except Exception as e:
        log.critical(e)
        return False, None

def decode_image(image_data):
    recv_data = image_data.encode()
    data = base64.b64decode(recv_data)
    img_data = np.asarray(bytearray(data),dtype='uint8')
    image = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    return image

def save_images(record_dir, camera_id, image):
    time_str = time.strftime('20%y%m%d_%H%M%S', time.localtime(time.time()))
    m_time_str = time_str + '_' + str(time.time()).split('.')[-1][:3]
    image_path = record_dir + '/' + str(camera_id) + '_' + m_time_str + '.jpg'
    cv2.imwrite(image_path, image)