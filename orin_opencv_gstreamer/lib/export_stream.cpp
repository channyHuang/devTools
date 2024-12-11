#include "export_stream.h"

#include <fstream>
#include "HGManager.h"

extern "C"

void setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode) {
    HGManager::getInstance()->setParams(pUri, nWidth, nHeight, pDecode);
}

extern "C"

bool startHGStream() {
    return HGManager::getInstance()->startPull();
}

extern "C"

bool stopHGStream() {
    return HGManager::getInstance()->stopPull();
}

extern "C"

void startPullRtsp(char* pUri, int nWidth, int nHeight)
{
    HGManager::getInstance()->startPullRtsp(pUri, nWidth, nHeight, nullptr);
}

extern "C"

void setCallback(CBFun_Callback pFunc, void *pUser)
{
    HGManager::getInstance()->setCallback(pFunc, pUser);
}

extern "C"

stCBResult* getFrame() {
    return HGManager::getInstance()->getFrame();
}