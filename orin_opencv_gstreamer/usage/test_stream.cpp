#include "export_stream.h"

#include <opencv2/opencv.hpp>

#include <thread>
#include <chrono>

bool openDirect(const char* pUri, char* decode = "H264") {
    cv::VideoCapture cap(pUri);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened" << std::endl;
        return false;
    }
    std::cout << __LINE__ << " open success" << std::endl;
    cap.release();
    return true;
}

bool openGstreamer(const char* pUri, char* decode) {
    std::ostringstream oss;
    if (std::strcmp(decode, "H264") == 0) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=2886, height=1919,format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink";
    } else if (std::strcmp(decode, "H265") == 0) {
        oss << "rtspsrc location=" << std::string(pUri) << " latency=100 ! rtph265depay ! h265parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=1920, height=1080,format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink";
    }
    cv::VideoCapture cap(oss.str(), cv::CAP_GSTREAMER);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened" << std::endl;
        return false;
    }
    std::cout << __LINE__ << " open success" << std::endl;
    cap.release();
    return true;
}


int main()
{
    char *pUri = "/home/channy/Documents/projects/devTools/EncodeDecode/data/HG_EncodeType.H265.mp4";
    // char *pUri = "rtsp://admin:@192.168.1.155:554";
    char *decode = "H264";

    // setParams(pUri, 2880, 1616, decode);
    setParams(pUri, 1920, 1080, nullptr);
    bool res = startHGStream();
    if (res == false) {
        std::cout << "failed " << std::endl;
    }

    int nFrameNum = 0;
    stCBResult* stResult = nullptr;
    while (true) {
        stResult = getFrame();
        if (stResult == nullptr) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

            continue;
        }
        nFrameNum++;
        if (nFrameNum >= 500) {
            std::cout << nFrameNum << " frames count " << std::endl;
            break;
        }
        cv::Mat frame(stResult->nHeight, stResult->nWidth, CV_8UC3, stResult->pFrame);
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

    stopHGStream();

    return 0;
}