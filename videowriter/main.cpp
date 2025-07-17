#include <iostream>
#include <map>
#include <vector>

#include <opencv2/opencv.hpp>

inline std::map<std::string, int> fourccByCodec() {
    std::map<std::string, int> mapFourcc;
    mapFourcc["h264"] = cv::VideoWriter::fourcc('H','2','6','4');
    mapFourcc["h265"] = cv::VideoWriter::fourcc('H','E','V','C');
    mapFourcc["mpeg2"] = cv::VideoWriter::fourcc('M','P','E','G');
    mapFourcc["mpeg4"] = cv::VideoWriter::fourcc('M','P','4','2');
    mapFourcc["mjpeg"] = cv::VideoWriter::fourcc('M','J','P','G');
    mapFourcc["vp8"] = cv::VideoWriter::fourcc('V','P','8','0');
    mapFourcc["yuv"] = cv::VideoWriter::fourcc('I','4','2','0');
    mapFourcc["flv"] = cv::VideoWriter::fourcc('V','L','V','1');
    return mapFourcc;
}

inline std::vector<std::string> extVideo() {
    std::vector<std::string> vExtVideo = {"mp4", "avi", "mkv"};
    return vExtVideo;
}

bool writeVideo(std::string sFourcc, std::string sExt, std::map<std::string, int> &mapFourcc, std::string &pUri) {
    printf("write video: %s.%s \n", sFourcc.c_str(), sExt.c_str());
    auto itr = mapFourcc.find(sFourcc);
    if (itr == mapFourcc.end()) return false;
    int nFourcc = itr->second;
    // int nWidth = 1280, nHeight = 720;

    cv::VideoCapture cap(pUri, cv::CAP_ANY);
    int nWidth = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    int nHeight = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    if (!cap.isOpened()) {
        std::cerr << "VideoCapture not opened:\nuri = " << pUri << std::endl;
        return 0;
    }

    std::string sOutputVideo = "WriteVideo_" + sFourcc + "." + sExt;
    cv::VideoWriter writer;
    writer.open(sOutputVideo, nFourcc, 30, cv::Size(nWidth, nHeight));
    cv::Mat feature = cv::Mat::zeros(nHeight, nWidth, CV_8UC3);
    cv::Mat frame;
    int nFrameNum = 0;
    while (cap.isOpened()) { 
        cap.read(frame);
        if (frame.rows <= 0 || frame.cols <= 0) {
            break;
        }

        for (int i = 0; i < nHeight; ++i) {
            for (int j = 0; j < nWidth; ++j) {
                feature.at<cv::Vec3b>(i, j)[0] = frame.at<cv::Vec3b>(i, j)[0];
                feature.at<cv::Vec3b>(i, j)[1] = frame.at<cv::Vec3b>(i, j)[1];
                feature.at<cv::Vec3b>(i, j)[2] = frame.at<cv::Vec3b>(i, j)[2];
            }
        }

        // for (int i = 0; i < nHeight; ++i) {
        //     for (int j = 0; j < nWidth; ++j) {
        //         feature.at<cv::Vec3b>(i, j)[0] = rand() % 256;
        //         feature.at<cv::Vec3b>(i, j)[1] = rand() % 256;
        //         feature.at<cv::Vec3b>(i, j)[2] = rand() % 256;
        //     }
        // }
        // cv::imshow("frame", feature);
        // cv::waitKey(1);
        writer.write(feature);

        nFrameNum++;
    }
    writer.release();
    cap.release();

    return true;
}

int main() {
    std::string pUri = "/home/channy/Documents/projects/WJ_restruct/video.avi";
    

    std::map<std::string, int> mapFourcc = fourccByCodec();
    std::vector<std::string> vExtVideos = extVideo();

    for (auto itr = mapFourcc.begin(); itr != mapFourcc.end(); itr++) {
        if (itr->first != "h265") continue;
        for (int i = 0; i < vExtVideos.size(); ++i) {
            writeVideo(itr->first, vExtVideos[i], mapFourcc, pUri);
            break;
        }
    }
    
    return 0;
}