#include "libExport.h"

int main()
{
    char *pUri = "rtsp://admin:@192.168.1.155:554";
    char *decode = "H264";

    setParams(pUri, 960, 540, decode);
    start();

    return 0;
}