# 图像编解码
## JPEG (Joint Photographic Experts Group)
```py
image = cv2.imread(sImgName)
res, data = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
data = np.array(data)
byteCount = data.shape[0]
```

## WebP
```py
image = cv2.imread(sImgName)
res, data = cv2.imencode('.webp', image, [int(cv2.IMWRITE_WEBP_QUALITY), 95])
data = np.array(data)
byteCount = data.shape[0]
```

## ICER
[ICER](https://github.com/TheRealOrange/icer_compression.git)

## CORN
[COIN](https://gitcode.com/gh_mirrors/coi/coin.git)
神经网络对每幅图像进行训练$${x,y} -> {r,g,b}$$生成网络参数作为传输数据

## Guetzli
主要对原始图像（JPEG或PNG）进行压缩成JPEG，对原JPEG算法的改进，没有改变解压算法

## SReC
[SReC](git@github.com:caoscott/SReC.git)
编译torchac需要特定版本的NVCC和GCC，直接在docker下运行更加方便。

使用1920x1080的大小为569.2KB的单张.jpg图像作为输入
```sh
python3 -um src.encode --path ./datasets/ --file ./datasets/images.txt --save-path ./ --load ./models/openimages.pth

python3 -um src.decode --path ./datasets/ --file ./datasets/srecs.txt --save-path ./datasets/ --load ./models/openimages.pth 
```
结果输出的.srec文件大小为12.5MB，解码后的.png图像大小为3.2MB

# 视频编解码
## H.265
```py
command = ('ffmpeg', '-ss', '10', '-i', sVideoName, '-vcodec', 'libx265', '-crf', '23', sOutVideoName)
subprocess.call(command)
```
## DVC/FVC/HLVC...

## DeepZip/DZip

# 语义分割
