#include <iostream>
#include <string>

#include "../lib/libExport.h"

#include <opencv2/opencv.hpp>

#include <thread>
#include <chrono>

int main()
{
    char *pUri = "rtsp://admin:@192.168.1.155:554";
    char *decode = "H264";

    setParams(pUri, 960, 540, decode);
    start();

    int nFrameNum = 0;
    stCBResult stResult;
    while (true) {
        bool res = getFrame(stResult);
        if (!res) {
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            continue;
        }
        nFrameNum++;
        if (nFrameNum >= 500) break;
        cv::Mat frame(stResult.nHeight, stResult.nWidth, CV_8UC3, stResult.pFrame);
        if (frame.empty()) {
            std::cerr << "err " << std::endl;
        }
        try {
            cv::imshow("imgs", frame);
            cv::waitKey(1);
        } catch (std::exception &e) {
            std::cout << e.what() << std::endl;
        }
    }

    stop();

    return 0;
}