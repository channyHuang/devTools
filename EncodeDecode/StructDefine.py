
from enum import Enum
import threading

class EncodeType(Enum):
    Origin = 1
    JPEG = 2
    Segment = 3
    WebP = 4
    H265 = 5

g_nHeight = 1080
g_nWidth = 1920

class StructDefine:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(StructDefine, "_instance"):
            with StructDefine._instance_lock:
                if not hasattr(StructDefine, "_instance"):
                    StructDefine._instance = object.__new__(cls)
        return StructDefine._instance

    def __init__(self):
        self.nHeight = 1080
        self.nWidth = 1920

structDefine = StructDefine()

if __name__ == '__main__':
    structDefine