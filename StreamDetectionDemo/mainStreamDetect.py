import cv2
import multiprocessing as mp
import threading
import time
import numpy as np

from InferenceYolo import InferenceYolo

# quDetect: [input_img, det, img_crops, time_stamp]
# detections: [[x1, y1, x2, y2, conf, label], ...]
class StreamDetect:
    def __init__(self, quStream = mp.Queue(maxsize=2), 
                quDetect = mp.Queue(maxsize = 2),
                quOutput = mp.Queue(maxsize = 2)):
        self.infer = InferenceYolo()

        detectThread = threading.Thread(target = self.detect, args = (quStream, quDetect, quOutput))
        detectThread.start()

    def detect(self, quStream = mp.Queue(maxsize=2), 
                quDetect = mp.Queue(maxsize = 2),
                quOutput = mp.Queue(maxsize = 2)):

        while True:
            try:
                if quStream.empty():
                    time.sleep(0.001)
                    continue
                recv_data = quStream.get()
                if quOutput.full():
                    _ = quOutput.get()
                quOutput.put(recv_data)

                start_time = time.time()
                mImageOrigin = recv_data[0]
                time_stamp = recv_data[1]

                mImageDet, classes, boxes, scores = self.infer.inference(mImageOrigin, True)

                vResultDetect = []
                for cls, box, score in zip(classes, boxes, scores):
                    vResultDetect.append([box[0], box[1], box[2], box[3], score, cls])
                vSendData = [mImageDet, vResultDetect]

                if quDetect.full():
                    quDetect.get()
                quDetect.put(vSendData)

            except:
                logger.info('error')

if __name__ == '__main__':
    from StreamEncodeDecode import StreamDecode
    quStreamList = [mp.Queue(maxsize = 2)]
    quDetect = mp.Queue(maxsize = 2)
    quOutput = mp.Queue(maxsize = 2)

    StreamDecode(quStreamList, './data/pedestrians.mp4')

    StreamDetect(quStreamList[0], quDetect, quOutput)

    width = 1920
    height = 1080
    bFirst = True
    origin_frame = None
    res_frame = None

    while True:
        if not quDetect.empty():
            detData = quDetect.get()

            res_frame = detData[0]
            # cv2.imshow('res', detData[0])
            # cv2.waitKey(1)
        if not quOutput.empty():
            streamData = quOutput.get()
            origin_frame = streamData[0]

            if bFirst:
                bFirst = False
                
                width = origin_frame.shape[1]
                height = origin_frame.shape[0]

            # cv2.imshow('origin', streamData[0])
            # cv2.waitKey(1)
        if origin_frame is not None and res_frame is not None:
            final_image = np.zeros((height, width * 2, 3), dtype = np.uint8)
            final_image[:, :width, :] = origin_frame
            final_image[:, width:, :] = res_frame
            cv2.imwrite('result.jpg', final_image)
        
        time.sleep(0.002)
