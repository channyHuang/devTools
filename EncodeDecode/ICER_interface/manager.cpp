#include "manager.h"

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <string>

#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_write.h"
#include "color_util.h"

Manager* Manager::m_pInstance = nullptr;

Manager::Manager() {}
Manager::~Manager() {}

void rgb888_packed_to_yuv(uint16_t *y_channel, uint16_t *u_channel, uint16_t *v_channel, uint8_t *img, size_t image_w, size_t image_h, size_t rowstride) {
    int32_t r, g, b;
    uint8_t *pixel;

    uint16_t *output_y, *output_u, *output_v;
    for (size_t row = 0;row < image_h;row++) {
        pixel = img + 3 * rowstride * row;
        output_y = y_channel + rowstride * row;
        output_u = u_channel + rowstride * row;
        output_v = v_channel + rowstride * row;
        for (size_t col = 0;col < image_w;col++) {
            r = pixel[0];
            g = pixel[1];
            b = pixel[2];

            *output_y = CRGB2Y(r, g, b);
            *output_u = CRGB2Cb(r, g, b);
            *output_v = CRGB2Cr(r, g, b);
            pixel += 3;
            output_y++; output_u++; output_v++;
        }
    }
}

void yuv_to_rgb888_packed(uint16_t *y_channel, uint16_t *u_channel, uint16_t *v_channel, uint8_t *img, size_t image_w, size_t image_h, size_t rowstride) {
    int32_t y, u, v;
    uint8_t *pixel;

    uint16_t *input_y, *input_u, *input_v;
    for (size_t row = 0;row < image_h;row++) {
        pixel = img + 3 * rowstride * row;
        input_y = y_channel + rowstride * row;
        input_u = u_channel + rowstride * row;
        input_v = v_channel + rowstride * row;
        for (size_t col = 0;col < image_w;col++) {
            y = *input_y;
            u = *input_u;
            v = *input_v;

            pixel[0] = CYCbCr2R(y, u, v);
            pixel[1] = CYCbCr2G(y, u, v);
            pixel[2] = CYCbCr2B(y, u, v);

            pixel += 3;
            input_y++; input_u++; input_v++;
        }
    }
}

bool Manager::encode(const char *pFileName, const char* pOutName, int &nWidth, int& nHeight, int &nChannel) {
    // loading image
    icer_init();
    uint8_t* pInData = stbi_load(pFileName, &nWidth, &nHeight, &nChannel, 3);
    if (pInData == nullptr) {
        return false;
    }
    // converting to yuv
    uint16_t *pCompress[3];
    for (int c = 0; c < nChannel; ++c) {
        pCompress[c] = (uint16_t *)malloc(nWidth * nHeight * 2);
    }
    rgb888_packed_to_yuv(pCompress[0], pCompress[1], pCompress[2], pInData, nWidth, nHeight, nWidth);
    // compress, 100kb
    const int nStreamSize = 100000;
    uint8_t *pStream = (uint8_t *)malloc((nStreamSize << 1) + 500);
    icer_output_data_buf_typedef output;
    icer_init_output_struct(&output, pStream, (nStreamSize << 1), nStreamSize);

    clock_t stBeginTime = clock();
    icer_compress_image_yuv_uint16(pCompress[0], pCompress[1], pCompress[2], nWidth, nHeight, m_nStages, m_eFilter, m_nSegments, &output);
    clock_t stEndTime = clock();

    // save result
    FILE *pFile = fopen(pOutName, "wb");
    size_t nWritenSize = fwrite(output.rearrange_start, sizeof(output.rearrange_start[0]), output.size_used, pFile);
    fflush(pFile);
    fclose(pFile);

    // release
    free(pStream);
    for (int c = 0; c < m_nChannel; ++c) {
        free(pCompress[c]);
    }
    stbi_image_free(pInData);

    return true;
}

bool Manager::decode(const char *pFileName, const char* pOutName, int nWidth, int nHeight, int nChannel) {
    // loading image
    size_t szWidth, szHeight;
    icer_init();

    size_t nBufferSize = 500;
    uint8_t *pBuffer = (uint8_t *)malloc(nBufferSize);
    FILE *pFile = fopen(pFileName, "rb");
    size_t nReadLength = 0;
    while (fread(pBuffer + nReadLength, sizeof *pBuffer, 1, pFile)) {
        if (nReadLength >= nBufferSize - 1) {
            nBufferSize += 500;
            pBuffer = (uint8_t*)realloc(pBuffer, nBufferSize);
        }
        nReadLength++;
    }
    fclose(pFile);

    // decompress
    uint16_t *pDecompress[3];
    uint8_t *pDisplay = (uint8_t *)malloc(nWidth * nHeight * nChannel);
    for (int c = 0; c <= m_nChannel; ++c) {
        pDecompress[c] = (uint16_t *)malloc(nWidth * nHeight * 2);
    }
    clock_t stBeginTime = clock();
    int res = icer_decompress_image_yuv_uint16(pDecompress[0], pDecompress[1], pDecompress[2], &szWidth, &szHeight, nWidth * nHeight, pBuffer, nReadLength, m_nStages, m_eFilter, m_nSegments);
    if (res != ICER_RESULT_OK) return false;
    clock_t stEndTime = clock();
    yuv_to_rgb888_packed(pDecompress[0], pDecompress[1], pDecompress[2], pDisplay, nWidth, nHeight, nWidth);

    // save result
    std::string sOutName = std::string(pOutName);
    size_t nPos = sOutName.find_last_of('.');
    if (nPos == std::string::npos) return false;
    std::string sEnd = sOutName.substr(nPos + 1);
    if (strcmp(sEnd.c_str(), "bmp") == 0) {
        res = stbi_write_bmp(pOutName, nWidth, nHeight, nChannel, pDisplay);
    } else if (strcmp(sEnd.c_str(), "jpg") == 0) {
        res = stbi_write_jpg(pOutName, nWidth, nHeight, nChannel, pDisplay, 95);
    } else if (strcmp(sEnd.c_str(), "png") == 0) {
        res = stbi_write_png(pOutName, nWidth, nHeight, nChannel, pDisplay, nWidth * nHeight * nChannel);
    }
    if (res == 0) return false;

    // release
    for (int c = 0; c < m_nChannel; ++c) {
        free(pDecompress[c]);
    }
    free(pDisplay);
    free(pBuffer);
    return true;
}

char* Manager::encodeData(const char *pData, int& nSize, int nWidth, int nHeight, int nChannel) {
    nSize = 0;
    uint8_t* pInData = (uint8_t*)pData;
    if (pInData == nullptr) {
        return nullptr;
    }
    printf("encodeData [w,h] = [%d, %d] size = %d\n", nWidth, nHeight, nSize);
    icer_init();
    // converting to yuv
    uint16_t *pCompress[3];
    for (int c = 0; c < nChannel; ++c) {
        pCompress[c] = (uint16_t *)malloc(nWidth * nHeight * 2);
    }
    rgb888_packed_to_yuv(pCompress[0], pCompress[1], pCompress[2], pInData, nWidth, nHeight, nWidth);
    // compress
    const int nStreamSize = 100000;
    uint8_t *pStream = (uint8_t *)malloc((nStreamSize << 1) + 500);
    icer_output_data_buf_typedef output;
    icer_init_output_struct(&output, pStream, (nStreamSize << 1), nStreamSize);

    clock_t stBeginTime = clock();
    icer_compress_image_yuv_uint16(pCompress[0], pCompress[1], pCompress[2], nWidth, nHeight, m_nStages, m_eFilter, m_nSegments, &output);
    clock_t stEndTime = clock();
    printf("compress time taken: %lf\n", (float)(stEndTime - stBeginTime)/CLOCKS_PER_SEC);

    nSize = output.size_used;
    char* pResult = (char*)malloc(output.size_used);
    memcpy(pResult, output.rearrange_start, output.size_used);
    printf("encodeData result size = %d\n", nSize);
    // release
    free(pStream);
    for (int c = 0; c < m_nChannel; ++c) {
        free(pCompress[c]);
    }
    // stbi_image_free(pInData);
    return pResult;
}

char* Manager::decodeData(const char *pData, int nSize, int nWidth, int nHeight, int nChannel) {
    icer_init();

    uint8_t *pBuffer = (uint8_t *)pData;
    int nReadLength = nSize;
    printf("decodeData [w,h] = [%d, %d] size = %d\n", nWidth, nHeight, nSize);

    // // decompress
    uint16_t *pDecompress[3];
    uint8_t *pDisplay = (uint8_t *)malloc(nWidth * nHeight * nChannel);
    for (int c = 0; c < m_nChannel; ++c) {
        pDecompress[c] = (uint16_t *)malloc(nWidth * nHeight * 2);
    }
    clock_t stBeginTime = clock();
    int res = icer_decompress_image_yuv_uint16(pDecompress[0], pDecompress[1], pDecompress[2], &m_nWidth, &m_nHeight, nWidth * nHeight, pBuffer, nReadLength, m_nStages, m_eFilter, m_nSegments);
    if (res != ICER_RESULT_OK) return nullptr;
    clock_t stEndTime = clock();
    printf("decompress time taken: %lf\n", (float)(stEndTime - stBeginTime)/CLOCKS_PER_SEC);

    yuv_to_rgb888_packed(pDecompress[0], pDecompress[1], pDecompress[2], pDisplay, m_nWidth, m_nHeight, m_nWidth);

    char* pResult = (char*)malloc(nWidth * nHeight * nChannel);
    memcpy(pResult, pDisplay, nWidth * nHeight * nChannel);

    // release
    for (int c = 0; c < m_nChannel; ++c) {
        free(pDecompress[c]);
    }
    free(pDisplay);
    // free(pBuffer);

    return pResult;
}
