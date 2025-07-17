#include <iostream>
#include <thread>

#include "sockpp/tcp_acceptor.h"
#include "sockpp/version.h"

using namespace std;

const std::string HTTP_RESPONSE =
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Content-Length: 13\r\n"
    "Connection: close\r\n"
    "\r\n"
    "Hello, World!";

void run_echo(sockpp::tcp_socket sock) {
    char buf[512];
    sockpp::result<size_t> res;

    while ((res = sock.read(buf, sizeof(buf))) && res.value() > 0)
        // sock.write_n(buf, res.value());
        sock.write_n(HTTP_RESPONSE.c_str(), HTTP_RESPONSE.length());
    cout << "Connection closed from " << sock.peer_address() << endl;
}

int main(int argc, char* argv[]) {
    cout << "Sample TCP echo server for 'sockpp' " << sockpp::SOCKPP_VERSION << '\n' << endl;

    // in_port_t port = (argc > 1) ? atoi(argv[1]) : sockpp::TEST_PORT;
    in_port_t port = 8081;

    sockpp::initialize();

    error_code ec;
    sockpp::tcp_acceptor acc{port, 4, ec};

    if (ec) {
        cerr << "Error creating the acceptor: " << ec.message() << endl;
        return 1;
    }
    cout << "Awaiting connections on port " << port << "..." << endl;

    while (true) {
        sockpp::inet_address peer;

        // Accept a new client connection
        if (auto res = acc.accept(&peer); !res) {
            cerr << "Error accepting incoming connection: " << res.error_message() << endl;
        }
        else {
            cout << "Received a connection request from " << peer << endl;
            sockpp::tcp_socket sock = res.release();

            // Create a thread and transfer the new stream to it.
            thread thr(run_echo, std::move(sock));
            thr.detach();
        }
    }

    return 0;
}