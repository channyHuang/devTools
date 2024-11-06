#include "HGManager.h"

#include <sstream>
#include <iostream>
#include <chrono>
#include <thread>

#include <opencv2/opencv.hpp>

HGManager* HGManager::m_pInstance = nullptr;

HGManager::HGManager() {}
HGManager::~HGManager() {}

void HGManager::setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode) {
    std::ostringstream oss;
    if (std::strcmp(pDecode, "H264") == 0) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=1920, height=1080,format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink";
    } else if (std::strcmp(pDecode, "H265") == 0) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph265depay ! h265parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=1920, height=1080,format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink";
    }
    m_sUri = oss.str();
    m_bInit = true;
}

bool HGManager::start() {
    if (!m_bInit || m_bRunning) {
        std::cerr << "Not init yeah or is running" << std::endl;
        return false;
    }
    cv::VideoCapture cap(m_sUri, cv::CAP_GSTREAMER);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened" << std::endl;
        return false;
    }
    cv::Mat frame;
    while (true) {
        cap.read(frame);
        cv::imshow("receiver", frame);
        if (cv::waitKey(1) == 27) {
            break;
        }
    }
    cv::destroyAllWindows();
    return true;
}

bool HGManager::stop() {
    if (!m_bInit || !m_bRunning) {
        std::cerr << "Not init yeah or not running" << std::endl;
        return false;
    }
    return true;
}

bool HGManager::startPullRtsp(char* pUri, int nWidth, int nHeight, const char* pDecode) {
    setParams(pUri, nWidth, nHeight, pDecode);
    cv::VideoCapture cap(m_sUri, cv::CAP_GSTREAMER);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened" << std::endl;
        return false;
    }
    cv::Mat frame;
    while (true) {
        cap.read(frame);
        cv::imshow("receiver", frame);
        if (cv::waitKey(1) == 27) {
            break;
        }
    }
    cv::destroyAllWindows();
}

void HGManager::setCallback(CBFun_Callback pFunc, void *pUser) {
    m_pFunc = pFunc;
    m_pUser = pUser;
}
