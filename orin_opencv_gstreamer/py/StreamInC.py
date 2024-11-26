from ctypes import *
import ctypes
import multiprocessing
import numpy as np
import time
import threading

class stCBResult(ctypes.Structure):
    _fields_ = [('pFrame', ctypes.c_void_p),
                ('nWidth', ctypes.c_int),
                ('nHeight', ctypes.c_int)]
    
class StreamInC():
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(StreamInC, "_instance"):
            with StreamInC._instance_lock:
                if not hasattr(StreamInC, "_instance"):
                    StreamInC._instance = object.__new__(cls)
        return StreamInC._instance
    
    def __init__(self):
        self.lib = None
        self.libpath = '../lib/build/libHGStreamLib.so'
        self.alive = multiprocessing.Manager().Value('b', False)

    def start(self, url):
        if self.lib is not None:
            return False
        
        self.lib = cdll.LoadLibrary(self.libpath)
        if self.lib is None:
            print('LoadLibrary failed', self.libpath)
            return False
        self.lib.setParams.argtypes = (ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
        self.lib.getFrame.restype = ctypes.POINTER(stCBResult)
        self.alive.value = True

        decode = 'H264'
        # self.lib.setParams(ctypes.c_char_p(url.encode('utf-8')), 1920, 1080, ctypes.c_char_p(decode.encode()))
        self.lib.setParams(url.encode(), 1920, 1080, decode.encode())
        self.lib.start()
        # stream_thread = threading.Thread(target = self.getFrame, args=())
        # stream_thread.start()
        # stream_thread.setDaemon(True)

        return True
         
    def stop(self):
        self.alive.value = False
        
        if self.lib is not None:
            self.lib.stop()

    def getFrame(self):
        if self.lib is None:
            return None
        stResult = self.lib.getFrame()
        if bool(stResult) == False or stResult.contents.pFrame is None:
            return None
        nWidth = stResult.contents.nWidth
        nHeight = stResult.contents.nHeight
        byteCount = nWidth * nHeight * 3
        imagePtr = ctypes.cast(stResult.contents.pFrame, ctypes.POINTER(ctypes.c_uint8 * byteCount))
        picture = np.frombuffer(imagePtr.contents, dtype=np.ubyte, count=byteCount)
        picture = np.reshape(picture, (nHeight, nWidth, 3))
        return picture

streamInC = StreamInC()

if __name__ == '__main__':
    import cv2
    streamInC.start('rtsp://admin:@192.168.1.155')

    while True:
        picture = streamInC.getFrame()
        time.sleep(1)

        if picture is None:
            time.sleep(0.1)
            continue
        cv2.imshow('res', picture)
        cv2.waitKey(1)
    cv2.destroyAllWindows()