#include <iostream>
#include <thread>

#include "export_icer.h"

#include "socketmanager.h"

#include <opencv2/opencv.hpp>

int main() {
    SocketManager::getInstance()->initReceiverSocket();

    std::string sRecvMessage;
    char *pDecodeData = nullptr;

    int nHeight = 1080;
    int nWidth = 1920;
    while (true) {
        sRecvMessage = SocketManager::getInstance()->getMessage();
        if (sRecvMessage.length() <= 0) {
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            continue;
        }
        printf("recv %s\n", sRecvMessage.c_str());
        pDecodeData = decodeData(sRecvMessage.c_str(), sRecvMessage.size(), nWidth, nHeight, 3);

        cv::Mat bufferMat(nHeight, nWidth, CV_8UC3, pDecodeData);
        cv::cvtColor(bufferMat, bufferMat, cv::COLOR_RGB2BGR);
        cv::imshow("image", bufferMat);
        cv::waitKey(1);
    }

    return 0;
}