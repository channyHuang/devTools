#include "libExport.h"

#include <fstream>
#include "HGManager.h"

extern "C"

void log(const char* pString)
{
    std::ofstream off("liblog.txt", std::ios::app);
    off << pString << std::endl;
    off.close();
}

void setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode) {
    HGManager::getInstance()->setParams(pUri, nWidth, nHeight, pDecode);
}

bool start() {
    HGManager::getInstance()->start();
}

bool stop() {
    HGManager::getInstance()->stop();
}

void startPullRtsp(char* pUri, int nWidth, int nHeight)
{
    HGManager::getInstance()->startPullRtsp(pUri, nWidth, nHeight);
}

void setCallback(CBFun_Callback pFunc, void *pUser)
{
    HGManager::getInstance()->setCallback(pFunc, pUser);
}
