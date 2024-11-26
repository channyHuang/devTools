#include "export.h"
#include <stdio.h>

#include "manager.h"

bool encode(const char *pFileName, const char* pOutName, int &nWidth, int& nHeight, int &nChannel) {
    return Manager::getInstance()->encode(pFileName, pOutName, nWidth, nHeight, nChannel);
}

bool decode(const char *pFileName, const char* pOutName, int nWidth, int nHeight, int nChannel) {
    return Manager::getInstance()->decode(pFileName, pOutName, nWidth, nHeight, nChannel);
}

char* encodeData(const char *pData, int& nSize, int nWidth, int nHeight, int nChannel) {
    return Manager::getInstance()->encodeData(pData, nSize,  nWidth, nHeight, nChannel);
}

char* decodeData(const char *pData, int nSize, int nWidth, int nHeight, int nChannel) {
    return Manager::getInstance()->decodeData(pData, nSize, nWidth, nHeight, nChannel);
}