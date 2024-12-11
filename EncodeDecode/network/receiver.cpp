

#include <iostream>
#include <thread>

#include "sockpp/udp6_socket.h"
#include "sockpp/udp_socket.h"
#include "sockpp/version.h"

using namespace std;

// --------------------------------------------------------------------------
// The thread function. This is run in a separate thread for each socket.
// Ownership of the socket object is transferred to the thread, so when this
// function exits, the socket is automatically closed.

template <typename UDPSOCK>
void run_echo(UDPSOCK sock) {
    char buf[512];

    // Each UDP socket type knows its address type as `addr_t`
    typename UDPSOCK::addr_t srcAddr;

    // Read some data, also getting the address of the sender,
    // then just send it back.
    while (true) {
        auto res = sock.recv_from(buf, sizeof(buf), &srcAddr);
        if (!res || res.value() == 0)
            break;

        printf("received %s\n", buf);
        // sock.send_to(buf, res.value(), srcAddr);
    }
}

// --------------------------------------------------------------------------
// The main thread creates the two UDP sockets (one each for IPv4 and IPv6),
// and then starts them running the echo function each in a separate thread.

int main(int argc, char* argv[]) {
    cout << "Sample UDP echo server for 'sockpp' " << sockpp::SOCKPP_VERSION << '\n' << endl;

    in_port_t port = (argc > 1) ? atoi(argv[1]) : sockpp::TEST_PORT;

    sockpp::initialize();

    sockpp::udp_socket udpsock;
    if (auto res = udpsock.bind(sockpp::inet_address("localhost", port)); !res) {
        cerr << "Error binding the UDP v4 socket: " << res.error_message() << endl;
        return 1;
    }

    sockpp::udp6_socket udp6sock;
    if (auto res = udp6sock.bind(sockpp::inet6_address("localhost", port)); !res) {
        cerr << "Error binding the UDP v6 socket: " << res.error_message() << endl;
        return 1;
    }

    // Spin up a thread to run the IPv4 socket.
    thread thr(run_echo<sockpp::udp_socket>, std::move(udpsock));
    thr.detach();

    // Run the IPv6 socket in this thread. (Call doesn't return)
    run_echo(std::move(udp6sock));
    return 0;
}
