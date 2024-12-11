
#ifndef EXPORT_STREAM_H
#define EXPORT_STREAM_H

#include <string.h>
#include <string>

#ifdef __cplusplus
#define D_EXTERN_C extern "C"
#else
#define D_EXTERN_C
#endif

#define __SHARE_EXPORT

#ifdef __SHARE_EXPORT
#define D_SHARE_EXPORT D_DECL_EXPORT
#else
#define D_SHARE_EXPORT D_DECL_IMPORT
#endif

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) || defined(__WIN32__)
#define D_CALLTYPE __stdcall
#define D_DECL_EXPORT __declspec(dllexport)
#define D_DECL_IMPORT
#else
#define __stdcall
#define D_CALLTYPE
#define D_DECL_EXPORT __attribute__((visibility("default")))
#define D_DECL_IMPORT __attribute__((visibility("default")))
#endif

// return struct
typedef struct stCBResult {
    // image
    unsigned char* pFrame = nullptr;
    // image width
    int nWidth = 0;
    // image height
    int nHeight = 0;
};

// definition of callback function
typedef void (__stdcall *CBFun_Callback)(stCBResult* stResult, void* pUser);

D_EXTERN_C D_SHARE_EXPORT void setParams(const char* pUri, int nWidth, int nHeight, const char* pDecode = "H264");

D_EXTERN_C D_SHARE_EXPORT bool startHGStream();

D_EXTERN_C D_SHARE_EXPORT bool stopHGStream();

D_EXTERN_C D_SHARE_EXPORT stCBResult* getFrame();

// start pull rtsp
D_EXTERN_C D_SHARE_EXPORT void startPullRtsp(char* pChar, int nWidth, int nHeight);

D_EXTERN_C D_SHARE_EXPORT void setCallback(CBFun_Callback pFunc, void *pUser);


#endif // EXPORT_STREAM_H