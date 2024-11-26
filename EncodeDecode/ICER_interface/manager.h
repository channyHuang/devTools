#pragma once

extern "C" {
#include "icer.h"
}

class Manager {
public:
    static Manager *getInstance() {
        if (m_pInstance == nullptr) {
            m_pInstance = new Manager();
        }
        return m_pInstance;
    }
    ~Manager();

    bool encode(const char *pFileName, const char* pOutName, int &nWidth, int& nHeight, int &nChannel);
    bool decode(const char *pFileName, const char* pOutName, int nWidth = 1920, int nHeight = 1080, int nChannel = 3);
    char* encodeData(const char *pData, int& nSize, int nWidth = 1920, int nHeight = 1080, int nChannel = 3);
    char* decodeData(const char *pData, int nSize, int nWidth = 1920, int nHeight = 1080, int nChannel = 3);

private:
    Manager();

private:
    static Manager *m_pInstance;

    size_t m_nWidth = 1920, m_nHeight = 1080;
    int m_nChannel = 3;
    int m_nStages = 4, m_nSegments = 10;
    enum icer_filter_types m_eFilter = ICER_FILTER_A;
};
