#include "HGManager.h"

#include <sstream>
#include <iostream>
#include <chrono>
#include <thread>

HGManager* HGManager::m_pInstance = nullptr;

HGManager::HGManager() {
    // std::cout << cv::getBuildInformation() << std::endl;
}
HGManager::~HGManager() {}

bool getCommandResult(const char* pCommand, std::string &sResult) {
    FILE *pFile = nullptr;
    char cBuffer[1024] = {0};
    sResult = "";
    // std::string sCommand = "gst-inspect-1.0 | grep omxh264dec";
    // std::string sCommand = "gst-inspect-1.0 | grep avdec_h264";
    if ((pFile = popen(pCommand, "r")) != nullptr) {
        while (!feof(pFile)) {
            memset(cBuffer, 0, 1024);
            if (fgets(cBuffer, 1024, pFile) != nullptr) {
                sResult += cBuffer;
            }
        }
        pclose(pFile);
    } else
        return false;
    return true;
}

bool hasGstreamerPlugin(const char* pPluginName = "omxh264dec") {
    std::string sCommand = "gst-inspect-1.0 | grep " + std::string(pPluginName);
    std::string sResult = "";
    bool res = getCommandResult(sCommand.c_str(), sResult);
    if (!res || sResult.size() <= 0) return false;
    return true;
}

void HGManager::setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode) {
    m_nHeight = nHeight;
    m_nWidth = nWidth;
    m_bInit = true;
    if (pDecode == nullptr) {
        m_sUri = std::string(pUri);
        m_bEnableGstreamer = false; 
        return;
    }

    std::ostringstream oss;
    if (hasGstreamerPlugin("omxh264dec")) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! video/x-raw, width=" << std::to_string(m_nWidth) << ", height=" << std::to_string(m_nHeight) << ", format=BGRx ! videoconvert ! appsink";
    } else if (hasGstreamerPlugin("omxh265dec")) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph265depay ! h265parse ! omxh265dec ! nvvidconv ! video/x-raw, width=" << std::to_string(m_nWidth) << ", height=" << std::to_string(m_nHeight) << ", format=BGRx ! videoconvert ! appsink";
    } else if (hasGstreamerPlugin("avdec_h264")) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink";
    } else if (hasGstreamerPlugin("avdec_h265")) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! appsink";
    } else if (hasGstreamerPlugin("nvv4l2decoder")) {
        if (std::strcmp(pDecode, "H264") == 0) {
            oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=" << std::to_string(m_nWidth) << ", height=" << std::to_string(m_nHeight) << ",format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink";
        } else if (std::strcmp(pDecode, "H265") == 0) {
            oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph265depay ! h265parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=1920, height=1080,format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink";
        }
    } else {
        std::cerr << "H.264 or H.265 decoder not found!" << std::endl;
        oss << std::string(pUri);
        m_sUri = oss.str();
        m_bEnableGstreamer = false;
        return;
    }
    m_bEnableGstreamer = true;
    m_sUri = oss.str();
    m_bInit = true;
}

bool HGManager::startPull() {
    if (!m_bInit || m_bRunning) {
        std::cerr << "Not init yeah or is running" << std::endl;
        return false;
    }
    run();
    return true;
}

bool HGManager::stopPull() {
    if (!m_bInit || !m_bRunning) {
        std::cerr << "Not init yeah or not running" << std::endl;
        return false;
    }
    stop();
    return true;
}

bool HGManager::startPullRtsp(char* pUri, int nWidth, int nHeight, const char* pDecode) {
    if (m_bRunning) {
        return false;
    }
    setParams(pUri, nWidth, nHeight, pDecode);
    run();
    return true;
}

void HGManager::setCallback(CBFun_Callback pFunc, void *pUser) {
    m_pFunc = pFunc;
    m_pUser = pUser;
}

bool HGManager::getFrame(stCBResult &stResult) {
    std::lock_guard<std::mutex> locker(mutex_buffer);
    if (m_quBuffer.empty()) return false;
    stResult = m_quBuffer.front();
    m_quBuffer.pop();
    return true;
}

void HGManager::threadLoop(std::future<void> exitListener) {
    cv::VideoCapture cap(m_sUri, m_bEnableGstreamer ? cv::CAP_GSTREAMER : cv::CAP_ANY);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened" << std::endl;
        return;
    }
    std::cout << __LINE__ << " open success " << m_sUri << std::endl;
    m_bRunning = true;
    do {
        cv::Mat frame;
        cap.read(frame);
        if (frame.rows <= 0 || frame.cols <= 0) {
            std::cerr << __LINE__ << "get frame failed " << std::endl;
            continue;
        }
        stCBResult stResult;
        stResult.pFrame = frame.data;
        stResult.nHeight = frame.rows;
        stResult.nWidth= frame.cols;
        std::lock_guard locker(mutex_buffer);
        if (!m_quBuffer.empty()) {
            m_quBuffer.pop();
        }
        m_quBuffer.push(stResult);
    } while (exitListener.wait_for(std::chrono::milliseconds(1)) == std::future_status::timeout);
    cap.release();
    m_bRunning = false;
}
