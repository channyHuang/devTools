Orin自带有安装GStreamer，使用OpenCV+GStreamer拉取H264视频流并显示。

原本使用的是
```sh
rtspsrc location=xxx_uri latency=100 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink
```
即使用`avdec_h264`发现延迟明显且积累越来越大，达5-6秒之久。

后改用
```sh
rtspsrc location=xxx_uri latency=100 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=1920, height=1080,format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink
```
即使用`nvv4l2decoder`略有改进，延迟1秒左右，但每间隔不定帧有明显一帧卡顿现象。

原因未知，暂记下问题。