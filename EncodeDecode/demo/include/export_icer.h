
#ifndef EXPORT_ICER_H
#define EXPORT_ICER_H

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

// 编解码文件
D_EXTERN_C D_SHARE_EXPORT bool encode(const char *pFileName, const char* pOutName, int &nWidth, int& nHeight, int &nChannel);
D_EXTERN_C D_SHARE_EXPORT bool decode(const char *pFileName, const char* pOutName, int nWidth, int nHeight, int nChannel);

// 编解码数据流
D_EXTERN_C D_SHARE_EXPORT char* encodeData(const char *pData, int &nSize, int nWidth, int nHeight, int nChannel);
D_EXTERN_C D_SHARE_EXPORT char* decodeData(const char *pData, int nSize, int nWidth, int nHeight, int nChannel);

#endif // EXPORT_ICER_H