#include "socketmanager.h"

#include <thread>

SocketManager* SocketManager::m_pInstance = nullptr;

SocketManager::SocketManager() {}
SocketManager::~SocketManager() {}

bool SocketManager::initSenderSocket(char* pUrl) {
    std::string sHost = "localhost";
    in_port_t nPort = sockpp::TEST_PORT;
    if (pUrl != nullptr) {
        std::string sUrl = std::string(pUrl);
        size_t pos = sUrl.find_last_of(":");
        if (pos == std::string::npos) {
            sHost = sUrl;
        } else {
            sHost = sUrl.substr(0, pos);
            nPort = atoi(sUrl.substr(pos + 1).c_str());
        }
    }

    sockpp::initialize();
    try {
        stSocket.connect(sockpp::inet_address(sHost, nPort));
    }
    catch (std::system_error& exc) {
        std::cerr << "Error connecting to server at " << sHost << ":" << nPort << "\n\t"
             << exc.what() << std::endl;
        return false;
    }
    std::cout << "Created UDP socket at: " << stSocket.address() << " " << sHost << " - " << nPort << std::endl;
    return true;
}

template <typename UDPSOCK>
void receiverCallback(UDPSOCK stSock) {
    char cBuffer[512];
    typename UDPSOCK::addr_t srcAddr;

    while (true) {
        auto res = stSock.recv_from(cBuffer, sizeof(cBuffer), &srcAddr);
        if (!res || res.value() == 0) break;
        // printf("receiverCallback %s\n", cBuffer);
        SocketManager::getInstance()->pushMessage(cBuffer, 0);
    }
}

bool SocketManager::initReceiverSocket(char* pUrl) {
    std::string sHost = "localhost";
    in_port_t nPort = sockpp::TEST_PORT;
    if (pUrl != nullptr) {
        std::string sUrl = std::string(pUrl);
        size_t pos = sUrl.find_last_of(":");
        if (pos == std::string::npos) {
            sHost = sUrl;
        } else {
            sHost = sUrl.substr(0, pos);
            nPort = atoi(sUrl.substr(pos + 1).c_str());
        }
    }

    sockpp::initialize();

    if (auto res = stSocket.bind(sockpp::inet_address("localhost", nPort)); !res) {
        std::cerr << "Error binding the UDP v4 socket: " << res.error_message() << std::endl;
        return false;
    }

    std::thread thr(receiverCallback<sockpp::udp_socket>, std::move(stSocket));
    thr.detach();

    return true;   
}

bool SocketManager::send(char* pMessage, size_t nSize) {
    auto res = stSocket.send(pMessage, nSize); 
    if (res != nSize) {
        std::cerr << "Error writing to the UDP socket: " << res.error_message() << std::endl;
        return false;
    }

    std::cout << "Send message (" << nSize << ") " << pMessage << std::endl;
    return true;
}

void SocketManager::pushMessage(char* pMessage, size_t nSize) {
    m_quRecvBuf.push(pMessage);
}

std::string SocketManager::getMessage() {
    if (m_quRecvBuf.empty()) return "";
    std::string sMessage = m_quRecvBuf.front();
    m_quRecvBuf.pop();
    return sMessage;
}