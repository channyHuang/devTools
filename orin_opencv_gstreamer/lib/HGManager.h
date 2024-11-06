#pragma once

#include <string>

#include "libExport.h"

class HGManager {
public:
    static HGManager* getInstance() {
        if (m_pInstance == nullptr) {
            m_pInstance = new HGManager();
        }
        return m_pInstance;
    }

    virtual ~HGManager();

    void setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode = "H264");
    bool start();
    bool stop();
    bool startPullRtsp(char* pUri, int nWidth, int nHeight, const char* pDecode = "H264");
    void setCallback(CBFun_Callback pFunc, void *pUser);

private:
    HGManager();

    static HGManager* m_pInstance;
    CBFun_Callback m_pFunc = nullptr;
    void* m_pUser = nullptr;
    bool m_bRunning = false, m_bInit = false;
    std::string m_sUri;
};
