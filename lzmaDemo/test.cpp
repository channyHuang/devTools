#include <iostream>
#include <fstream>
#include <string.h>

#include <lzma.h>

#define BUFSIZ 8192

void readFileData(const std::string &sFileName, unsigned char* &pData, size_t &nDataLen) {
    // read compressed data from file
    std::ifstream file(sFileName.c_str(), std::ios_base::in | std::ios_base::binary);
    if (!file) {
        printf("Open file failed [%s]\n", sFileName.c_str());
        return;
    }

    file.seekg(0, std::ios::end);
    nDataLen = file.tellg();
    file.seekg(0); 

	if (pData != nullptr) {
		delete []pData;
		pData = nullptr;
	}
    pData = new unsigned char[nDataLen];

    file.read((char*)pData, nDataLen);
    auto nReadByte = file.gcount();
	file.close();
    if (static_cast<size_t>(nReadByte) != nDataLen) {
        printf("Read file failed [%s]\n", sFileName.c_str());
        return;
    }    
    printf("Read file len = [%u]\n", nDataLen);
}

void writeFileData(const std::string &sFileName, const unsigned char* pData, size_t nDataLen) {
    // read compressed data from file
    std::ofstream file(sFileName.c_str(), std::ios_base::out | std::ios_base::binary);
    if (!file) {
        printf("Open file failed [%s]\n", sFileName.c_str());
        return;
    }

    file.write((char*)(pData), nDataLen);
	file.close();
	printf("Write file len = [%u]\n", nDataLen);
}

int encodeDecode(unsigned char* pData, size_t nDataLen, unsigned char* &pOutData, size_t &nOutDataLen, bool bEncode = true) {
	lzma_stream strm = LZMA_STREAM_INIT;
	lzma_ret ret = LZMA_OK;
	if (bEncode) {
		ret = lzma_easy_encoder(&strm, LZMA_PRESET_DEFAULT, LZMA_CHECK_CRC64);
	} else {
		ret = lzma_stream_decoder(&strm, UINT64_MAX, LZMA_CONCATENATED);
	}

	if (ret != LZMA_OK) {
		return -1;
	}
	uint8_t outbuf[nDataLen * 2];
	
	strm.next_in = (uint8_t*)pData;
	strm.avail_in = nDataLen;
	strm.next_out = outbuf;
	strm.avail_out = sizeof(outbuf);
	printf("*** %u\n", strm.avail_in);

	ret = lzma_code(&strm, LZMA_FINISH);
	if (strm.avail_out == 0 || ret == LZMA_STREAM_END) {
		nOutDataLen = sizeof(outbuf) - strm.avail_out;
		printf("-----bEncode = %d, nOutDataLen = %u\n", bEncode, nOutDataLen);
		if (pOutData != nullptr) {
			delete []pOutData;
			pOutData = nullptr;
		}
		pOutData = new unsigned char[nOutDataLen];
		memcpy((uint8_t*)pOutData, outbuf, nOutDataLen);
	} else if (ret != LZMA_OK) {
		printf("error! ret = %d\n", ret);
	} else {
		printf("ret = %d, strm.avail_out = %d\n", ret, strm.avail_out);
	}
	lzma_end(&strm);
	if (ret != LZMA_OK && ret != LZMA_STREAM_END) return -1;
	return 0;
}

int main() {
	unsigned char* pData = nullptr;
	size_t nDataLen = 0;
	unsigned char* pOutData = nullptr;
	size_t nOutDataLen = 0;
	unsigned char* pFinalData = nullptr;
	size_t nFinalDataLen = 0;

	std::string sFileName = "./input.pdf";
	readFileData(sFileName, pData, nDataLen);
	encodeDecode(pData, nDataLen, pOutData, nOutDataLen, true);
	printf("encode result : %d\n", nOutDataLen);
	writeFileData("./compress.bin", pOutData, nOutDataLen);

	int res = encodeDecode(pOutData, nOutDataLen, pFinalData, nFinalDataLen, false);
	printf("decode %d %d\n", nFinalDataLen, res);

	writeFileData("./out.pdf", pFinalData, nFinalDataLen);

	return 0;
}