# 使用icer对图像编解码
[icer](https://github.com/TheRealOrange/icer_compression.git)

* 编译出现undefined reference，在确认target_link_libraries增加了icer后依旧报错，最后发现是C/C++混合编译问题，需要对C实现增加"extern \"C\""
```c++
extern "C" {
#include "icer.h"
}
```

* 在malloc时越界不报错，但运行后会出现栈溢出错误，且是在运行完整个函数后报错
```c++
    uint16_t *pDecompress[3];
    uint8_t *pDisplay = (uint8_t *)malloc(nWidth * nHeight * nChannel);
    // 这里初始化申请内存时一开始把“<”误写成了“<=”，每次运行完整个函数后才报且必报栈溢出错误
    for (int c = 0; c < m_nChannel; ++c) {
        pDecompress[c] = (uint16_t *)malloc(nWidth * nHeight * 2);
    }
```

```sh
decompress time taken: 0.347728
*** stack smashing detected ***: terminated
Aborted (core dumped)
```

# stb_image读图像得到的data和OpenCV读图像得到的data不完全一样
```c++
// stb_image 读图像得到data
data = stbi_load(filename, &src_w, &src_h, &n, 3);

// OpenCV　读图像得到cvImg.data
cv::Mat cvImage = cv::imread(sInFile, cv::IMREAD_UNCHANGED);
cv::Mat cvImg = cvImage;
cv::cvtColor(cvImage, cvImg, cv::COLOR_BGR2RGB);
int nSize = strlen((char*)cvImg.data);
```
OpenCV直接读取的图像为BGR格式，在长度上就和stb_image读取的数据长度不一样。

把OpenCV读取的数据改成RGB格式后，长度和stb_image的一样，但具体的字符依旧有部分不一样。不过同样可以使用该编解码算法，中间生成的压缩数据长度也不一样，恢复后的图像从肉眼上看是相同的。
