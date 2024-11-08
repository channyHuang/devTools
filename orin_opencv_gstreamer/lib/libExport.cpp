#include "libExport.h"

#include <fstream>
#include "HGManager.h"

extern "C"

void setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode) {
    HGManager::getInstance()->setParams(pUri, nWidth, nHeight, pDecode);
}

bool start() {
    HGManager::getInstance()->startPull();
}

bool stop() {
    HGManager::getInstance()->stopPull();
}

void startPullRtsp(char* pUri, int nWidth, int nHeight)
{
    HGManager::getInstance()->startPullRtsp(pUri, nWidth, nHeight);
}

void setCallback(CBFun_Callback pFunc, void *pUser)
{
    HGManager::getInstance()->setCallback(pFunc, pUser);
}

bool getFrame(stCBResult &stResult) {
    HGManager::getInstance()->getFrame(stResult);
}