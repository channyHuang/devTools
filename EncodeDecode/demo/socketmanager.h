#include <iostream>
#include <queue>

#include "sockpp/udp_socket.h"
#include "sockpp/version.h"

class SocketManager {
public:
    static SocketManager *getInstance() {
        if (m_pInstance == nullptr) {
            m_pInstance = new SocketManager();
        }
        return m_pInstance;
    }
    ~SocketManager();

    bool initSenderSocket(char* pUrl = nullptr);
    bool initReceiverSocket(char* pUrl = nullptr);
    bool send(char* pMessage, size_t nSize);

    void pushMessage(char* pMessage, size_t nSize);
    std::string getMessage();

private:
    SocketManager();
    static SocketManager* m_pInstance;

    sockpp::udp_socket stSocket;
    std::queue<std::string> m_quRecvBuf;
    
};
