#include <iostream>

#include "export_icer.h"

#ifdef USE_OPENCV
#include <opencv2/opencv.hpp>
#endif

int main(int argc, char** argv) {
    if (argc < 4) return -1;
    std::string sInFile = std::string(argv[1]);
    std::string sOutFile = std::string(argv[2]);
    std::string sDecFile = std::string(argv[3]);

    int nWidth = 1920, nHeight = 1080, nChannel = 3;
    bool res = encode(sInFile.c_str(), sOutFile.c_str(), nWidth, nHeight, nChannel);
    std::cout << res << " encode " << nWidth << " " << nHeight << " " << nChannel << std::endl;
    decode(sOutFile.c_str(), sDecFile.c_str(), nWidth, nHeight, nChannel);
    std::cout << "decode end" << std::endl;


#ifdef USE_OPENCV
    cv::Mat cvImage = cv::imread(sInFile, cv::IMREAD_UNCHANGED);
    cv::Mat cvImg = cvImage;
    cv::cvtColor(cvImage, cvImg, cv::COLOR_BGR2RGB);
    int nSize = strlen((char*)cvImg.data);
    char* pEncoded = encodeData((char*)cvImg.data, nSize, nWidth, nHeight, nChannel);
    std::cout << "encode data " << nSize << " " << nWidth << std::endl;

    char *pData = decodeData(pEncoded, nSize, nWidth, nHeight, nChannel);

    cv::Mat bufferMat(nHeight, nWidth, CV_8UC3, pData);
    cv::cvtColor(bufferMat, bufferMat, cv::COLOR_RGB2BGR);
    cv::imshow("image", bufferMat);
    cv::waitKey(1000);
#endif

    return 0;
}