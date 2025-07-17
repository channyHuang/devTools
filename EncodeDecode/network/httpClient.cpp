#include <iostream>
#include <string>
#include "sockpp/tcp_connector.h"

int main() {
    // 创建一个 TCP 连接器
    sockpp::tcp_connector connector;

    // 连接到服务器
    auto res = connector.connect(sockpp::inet_address("127.0.0.1", 8081));
    if (!res) {
        std::cerr << "连接失败: " << res.error_message() << std::endl;
        return 1;
    }

    // 构建 HTTP GET 请求
    std::string request = "GET / HTTP/1.1\r\n"
                          "Host: 127.0.0.1\r\n"
                          "Connection: close\r\n"
                          "\r\n";

    // 发送 HTTP 请求
    auto resWrite = connector.write(request) ;
    if (resWrite != (size_t)request.length()) {
        std::cerr << "发送请求失败: " << resWrite.error_message() << std::endl;
        return 1;
    }

    // 接收 HTTP 响应
    char buffer[4096];
    ssize_t n;
    while (resWrite = connector.read(buffer, sizeof(buffer))) {
        if (!resWrite) {
            std::cerr << "读取响应失败: " << resWrite.error_message() << std::endl;
            return 1;
        }
        std::cout.write(buffer, resWrite.value());
    }

    // 关闭连接
    connector.close();

    return 0;
}
