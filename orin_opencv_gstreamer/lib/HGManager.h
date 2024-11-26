#pragma once

#include <string>
#include <mutex>
#include <queue>

#include "libExport.h"
#include "stopthread.h"

#include <opencv2/opencv.hpp>

class HGManager : public StopThread {
public:
    static HGManager* getInstance() {
        if (m_pInstance == nullptr) {
            m_pInstance = new HGManager();
        }
        return m_pInstance;
    }

    virtual ~HGManager();

    void setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode = "H264");
    bool startPull();
    bool stopPull();
    bool startPullRtsp(char* pUri, int nWidth, int nHeight, const char* pDecode = nullptr);
    void setCallback(CBFun_Callback pFunc, void *pUser);

    stCBResult* getFrame();

protected:
    virtual void threadLoop(std::future<void> exitListener);

private:
    HGManager();

    static HGManager* m_pInstance;
    CBFun_Callback m_pFunc = nullptr;
    void* m_pUser = nullptr;
    bool m_bRunning = false, m_bInit = false;
    std::string m_sUri;
    bool m_bEnableGstreamer = true;
    int m_nWidth = 1920, m_nHeight = 1080;

    std::mutex mutex_buffer;
    std::queue<stCBResult*> m_quBuffer;
};
