import cv2
from enum import Enum, unique
import logging
import multiprocessing as mp
import numpy as np
import os
import subprocess
import threading
import time

from VisionUtil import splitDirFiles

image_width = 960
image_height = 540

logging.basicConfig(
    level = logging.INFO,
    format= '%(asctime)s [%(levelname)s] %(name)s  - %(message)s',
    filename = __file__ + '.log'
)
logger = logging.getLogger(__name__)

@unique
class StreamMode(Enum):
    Camera_Id_List = 0
    Camera_Id = 1
    Video = 2
    Videos_Dir = 3

def rtspDecodeByGstream(uri, width, height, latency, Decoder='H264'):
    """Open an RTSP URI (IP CAM)."""
    gst_elements = str(subprocess.check_output('gst-inspect-1.0'))
    if 'omxh264dec' in gst_elements:
        # Use hardware H.264 decoder on Jetson platforms
        gst_str = ('rtspsrc location={} latency={} ! '
                   'rtph264depay ! h264parse ! omxh264dec ! '
                   'nvvidconv ! '
                   'video/x-raw, width=(int){}, height=(int){}, '
                   'format=(string)BGRx ! videoconvert ! '
                   'appsink').format(uri, latency, width, height)
    elif 'avdec_h264' in gst_elements:
        # Otherwise try to use the software decoder 'avdec_h264'
        # NOTE: in case resizing images is necessary, try adding
        #       a 'videoscale' into the pipeline
        gst_str = ('rtspsrc location={} latency={} ! '
                   'rtph264depay ! h264parse ! avdec_h264 ! '
                   'videoconvert ! appsink').format(uri, latency)
    elif 'omxh265dec' in gst_elements:
        # Use hardware H.264 decoder on Jetson platforms
        gst_str = ('rtspsrc location={} latency={} ! '
                   'rtph265depay ! h265parse ! omxh265dec ! '
                   'nvvidconv ! '
                   'video/x-raw, width=(int){}, height=(int){}, '
                   'format=(string)BGRx ! videoconvert ! '
                   'appsink').format(uri, latency, width, height)
    elif 'avdec_h265' in gst_elements:
        # Otherwise try to use the software decoder 'avdec_h264'
        # NOTE: in case resizing images is necessary, try adding
        #       a 'videoscale' into the pipeline
        gst_str = ('rtspsrc location={} latency={} ! '
                   'rtph265depay ! h265parse ! avdec_h265 ! '
                   'videoconvert ! appsink').format(uri, latency)
    elif 'nvv4l2decoder' in gst_elements:
        # Otherwise try to use the software decoder 'avdec_h264'
        # NOTE: in case resizing images is necessary, try adding
        #       a 'videoscale' into the pipeline
        if Decoder == 'H264':
            gst_str = (
                'rtspsrc location={} latency={} ! '
                'rtph264depay ! h264parse ! nvv4l2decoder ! '
                'nvvidconv ! '
                'video/x-raw, width={}, height={},format=BGRx ! '
                'videoconvert !'
                'video/x-raw, format=BGR ! '
                'appsink').format(uri, latency, width, height)
        elif Decoder == 'H265':
            gst_str = (
                'rtspsrc location={} latency={} ! '
                'rtph265depay ! h265parse ! nvv4l2decoder ! '
                'nvvidconv ! '
                'video/x-raw, width={}, height={},format=BGRx ! '
                'videoconvert !'
                'video/x-raw, format=BGR ! '
                'appsink').format(uri, latency, width, height)
    else:
        raise RuntimeError('H.264 or H.265 decoder not found!')
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def rtspEncodeByGstream(width = 960, height = 540, port=8888, 
                        factory_name='/detected',
                        Encoder='H265'):
    print('video encode')
    global out_send
    # out_send = cv2.VideoWriter('appsrc is-live=true ! videoconvert ! \
    #                             omxh264enc bitrate=12000000 ! video/x-h264, \
    #                             stream-format=byte-stream ! rtph264pay pt=96 ! \
    #                             udpsink host=192.168.10.121 port=5400 async=false',  # RTSP发布地址参数
    #                            cv2.CAP_GSTREAMER, 0, 15, (width, height), True)  # 视频帧率 分辨率
    if Encoder == 'H265':
        out_send = cv2.VideoWriter('appsrc!'
                                   'videoconvert! video/x-raw,format=BGRx ! '
                                   'nvvidconv ! '
                                   'nvv4l2h265enc bitrate=1200000 '
                                   'insert-sps-pps=1 idrinterval=30 insert-vui=1 !'
                                   'rtph265pay name=pay0 pt=96 !'
                                   'udpsink host=192.168.10.121 port=5400',  # RTSP发布地址参数
                                   cv2.CAP_GSTREAMER, 0, fps, (width, height), True)  # 视频帧率 分辨率
    elif Encoder == 'H264':
        out_send = cv2.VideoWriter('appsrc!'
                                   'videoconvert! video/x-raw,format=BGRx ! '
                                   'nvvidconv ! '
                                   'nvv4l2h264enc bitrate=1200000 '
                                   'insert-sps-pps=1 idrinterval=30 insert-vui=1 !'
                                   'rtph264pay name=pay0 pt=96 !'
                                   'udpsink host=192.168.10.121 port=5400',  # RTSP发布地址参数
                                   cv2.CAP_GSTREAMER, 0, fps, (width, height), True)  # 视频帧率 分辨率

    if not out_send.isOpened():
        print('VideoWriter not opened')
        exit(0)

    rtsp_port_num = port

    server = GstRtspServer.RTSPServer.new()
    server.props.service = "%d" % rtsp_port_num
    server.attach(None)

    factory = GstRtspServer.RTSPMediaFactory.new()
    if Encoder == 'H265':
        factory.set_launch("(udpsrc name=pay0 port=5400 buffer-size=5242880 \
                            caps=\"application/x-rtp, media=video, clock-rate=9000000, \
                            encoding-name=H265, payload=96 \")")
    elif Encoder == 'H264':
        factory.set_launch("(udpsrc name=pay0 port=5400 buffer-size=5242880 \
                            caps=\"application/x-rtp, media=video, clock-rate=9000000, \
                            encoding-name=H264, payload=96 \")")

    factory.set_shared(True)
    server.get_mount_points().add_factory(factory_name, factory)

    print("\n *** Launched RTSP Streaming at rtsp://192.168.10.121:%d/detected \n" % rtsp_port_num)
    return out_send

class StreamDecode:
    def __init__(self, vStreamQueueList = [mp.Queue(maxsize=2)], 
                sVideoPath = 'rtsp://admin:123456@192.168.0.168', 
                eVideoMode = StreamMode.Video, 
                nFps = 30, 
                bWarmup = False, 
                decoder='H264'):
        vVideosShuffix = [".mp4",".avi"]

        self.eMode = eVideoMode 
        self.sVideoPath = sVideoPath
        self.nBatchSize =  len(vStreamQueueList)
        self.nFps = nFps
        self.bWarmup = bWarmup
        self.decoder = decoder
        
        vVideoList = []
        if os.path.splitext(sVideoPath)[-1] in vVideosShuffix:
            self.eMode = StreamMode.Video
            vVideoList.append([sVideoPath])
        elif os.path.isdir(sVideoPath):  # one dir
            self.eMode = StreamMode.Videos_Dir
            vVideoList = splitDirFiles(sVideoPath, self.nBatchSize)
        elif isinstance(sVideoPath, (list, tuple)):
            self.eMode = StreamMode.Camera_Id_List
            for id in sVideoPath:
                vVideoList.append([id])
        else:
            self.eMode = StreamMode.Camera_Id
            vVideoList.append([video_path])
        
        logger.info(f'Stream Input: queue size = {self.nBatchSize} video list size = {len(vVideoList)}, mode = {self.eMode}')
        self.nBatchSize = min(self.nBatchSize, len(vVideoList))
        
        vThreads = [threading.Thread(target = self.getRtspSourceSingle, args = (vStreamQueueList[i], vVideoList[i])) for i in range(self.nBatchSize)] 
        
        for thread in vThreads:
            thread.start()
    
    def getRtspSourceSingle(self, stream_queue = mp.Queue(maxsize=2), vVideoList = []):
        last_time = time.time()
        skip_time = 1. / self.nFps

        if self.bWarmup:
            warmup_video = vVideoList[0]
            vVideoList.insert(0, warmup_video)
        
        for i, v in enumerate(vVideoList):
            sWindowName = os.path.split(v)[-1]
            if self.bWarmup and i == 0: # warmup model and others
                sWindowName = "warmup_{}".format(sWindowName)
            
            if ((self.eMode == StreamMode.Video) or (self.eMode == StreamMode.Videos_Dir)):
                cap = cv2.VideoCapture(v)
            else:
                cap = rtspDecodeByGstream(uri = v, width = image_width, height = image_height, latency=100, Decoder = self.decoder)#'H265'

            if not cap.isOpened():
                logger.error(f'get_rtsp_source_single failed: video = {v}')
                
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cur_time = time.time()
                    while cur_time - last_time < skip_time: # waiting
                        time.sleep(0.002)  # 2ms
                        cur_time = time.time()
                    last_time = cur_time

                    frame = cv2.resize(frame, (image_width, image_height))
                    send_data = [frame, cur_time, "000" if self.eMode == StreamMode.Camera_Id else sWindowName]
                    if stream_queue.full():
                        _ = stream_queue.get()
                    stream_queue.put(send_data)
                elif ((self.eMode == StreamMode.Video) or (self.eMode == StreamMode.Videos_Dir)):
                    break
                else:
                    loggger.error('get_rtsp_source_single failed, ret = ', ret)

if __name__ == '__main__':
    nBatchSize = 1
    vStreamQueueList = [mp.Queue(maxsize=2) for _ in range(nBatchSize)]
    # stream_decode = StreamDecode(vStreamQueueList, 'rtsp://admin:123456@192.168.0.168')
    stream_decode = StreamDecode(vStreamQueueList, './data/pedestrians.mp4')
    #writer = rtsp_stream_encode(width = 500, height = 500)

    while True:
        for qu in vStreamQueueList:
            if qu.empty():
                time.sleep(0.1)
                continue
            data = qu.get()
            cv2.imshow(data[2], data[0])
            cv2.waitKey(1)
            #writer.write(stream_data[0])
    cv2.destroyAllWindows()            
