#include <iostream>
#include <thread>

#include "export_icer.h"
#include "export_stream.h"

#include "socketmanager.h"

#include <opencv2/opencv.hpp>

void allInOne() {
    char *pUri = "/home/channy/Documents/datasets/1120数据/DJI_202411201519_053/DJI_20241120152234_0001_W.MP4";
    char *decode = "H264";
    int nWidth = 1920, nHeight = 1080;
    const int nReWidth = 640, nReHeight = 360;

    int nFrameNum = 0;
    cv::VideoCapture cap(pUri, cv::CAP_ANY);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened:\nuri = " << pUri << std::endl;
        return;
    }

    int nPadding = 256;
    cv::VideoWriter writer;
    writer.open("./feature.avi", cv::VideoWriter::fourcc('H', '2', '6', '4'), 30, cv::Size(nPadding, nPadding));
    while (cap.isOpened()) {
        cv::Mat frame;
        cap.read(frame);
        if (frame.rows <= 0 || frame.cols <= 0) {
            break;
            std::cerr << __LINE__ << "get frame failed " << std::endl;
            continue;
        }

        cv::Mat allFrame = cv::Mat::zeros(nReHeight, nReWidth * 2 + 128, CV_8UC3);
        cv::Mat showFrame = frame.clone();
        cv::resize(showFrame, showFrame, cv::Size(nReWidth, nReHeight));
        showFrame.copyTo(allFrame(cv::Rect(0, 0, nReWidth, nReHeight)), showFrame);
        // cv::imshow("origin", allFrame);
        // cv::waitKey(1);
        nFrameNum++;
        cv::Mat cvImg = frame.clone();
        cv::cvtColor(cvImg, cvImg, cv::COLOR_BGR2RGB);

        // if (nFrameNum % 100 == 0) {
        // }

        int nSize = strlen((char*)cvImg.data);
        if (nSize <= 0) continue;

        char* pEncoded = encodeData((char*)cvImg.data, nSize, nWidth, nHeight, 3);
        
        char *pData = decodeData(pEncoded, nSize, nWidth, nHeight, 3);
        
        cv::Mat feature = cv::Mat::zeros(256, 256, CV_8UC3);
        for (int i = 0; i < nPadding; ++i) {
            for (int j = 0; j < nPadding; ++j) {
                feature.at<cv::Vec3b>(i, j)[0] = pData[(i * nPadding + j) % nSize];
                feature.at<cv::Vec3b>(i, j)[1] = pData[(i * nPadding + j) % nSize];
                feature.at<cv::Vec3b>(i, j)[2] = pData[(i * nPadding + j) % nSize];
            }
        }
        // feature.copyTo(allFrame(cv::Rect(nReWidth, 0, 128, nReHeight)), feature);
        
        cv::Mat bufferMat(nHeight, nWidth, CV_8UC3, pData);
        cv::cvtColor(bufferMat, bufferMat, cv::COLOR_RGB2BGR);

        cv::Mat showBuffer = bufferMat.clone();
        cv::resize(showBuffer, showBuffer, cv::Size(nReWidth, nReHeight));
        showBuffer.copyTo(allFrame(cv::Rect(nReWidth + 128, 0, nReWidth, nReHeight)), showBuffer);

        // writer.write(allFrame);
        writer.write(feature);

        // if (nFrameNum % 100 == 0) {
        //     cv::imwrite("./" + std::to_string(nFrameNum) + ".jpg", allFrame);
        // }
        // char name[10];
        // sprintf(name, "%03d.jpg\n", nFrameNum);
        // cv::imwrite("./tmp/" + std::string(name), allFrame);

        // if (nFrameNum >= 410) break;
    }
    cap.release();
    writer.release();
}

void sendRecv() {
    char *pUri = "/home/channy/Documents/datasets/1120数据/多异源图像自动配准/草地场景/DJI_20241120152234_0001_W.MP4";
    char *decode = "H264";
    int nWidth = 1920, nHeight = 1080;
    
    setParams(pUri, 1920, 1080, nullptr);
    bool res = startHGStream();
    if (res == false) {
        std::cout << "failed " << std::endl;
    }

    SocketManager::getInstance()->initSenderSocket();

    int nFrameNum = 0;
    stCBResult* stResult = nullptr;
    int nGetFrameFailCount = 0;
    while (true) {
        stResult = getFrame();
        if (stResult == nullptr || stResult->pFrame == nullptr) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            nGetFrameFailCount++;
            if (nGetFrameFailCount >= 10) break;
            continue;
        }
        nGetFrameFailCount = 0;
        nFrameNum++;
        if (nFrameNum >= 99999) nFrameNum = 0;

        int nSize = strlen((char*)stResult->pFrame);
        printf("get frame %d size = %d\n", nFrameNum, nSize);
        char* pEncoded = encodeData((char*)stResult->pFrame, nSize, stResult->nWidth, stResult->nHeight, 3);
        
        SocketManager::getInstance()->send((char*)pEncoded, nSize);

        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    stopHGStream();
}

int main() {
    // char *pUri = "rtsp://admin:@192.168.1.155:554";
    // char *decode = "H264";
    allInOne();

    return 0;
}