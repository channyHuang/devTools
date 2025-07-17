# 定时器
import time

if __name__ == '__main__':
    targetTime = 10 * 60
    starttime = time.time()
    curtime = None
    while True:
        curtime = time.time()
        duration = (int)(curtime - starttime)
        print('\r{:02d}:{:02d}'.format((int)(duration / 60), duration % 60), end = '', flush = True)
        if duration >= targetTime:
            break
    