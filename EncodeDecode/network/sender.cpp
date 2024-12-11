#include <iostream>

#include "sockpp/udp_socket.h"
#include "sockpp/version.h"

using namespace std;

int main(int argc, char** argv) {
    cout << "Sample UDP echo client for 'sockpp' " << sockpp::SOCKPP_VERSION << '\n' << endl;

    string host = (argc > 1) ? argv[1] : "localhost";
    in_port_t port = (argc > 2) ? atoi(argv[2]) : sockpp::TEST_PORT;

    sockpp::initialize();

    sockpp::udp_socket sock;

    try {
        sock.connect(sockpp::inet_address(host, port));
    }
    catch (system_error& exc) {
        cerr << "Error connecting to server at " << host << ":" << port << "\n\t"
             << exc.what() << endl;
        return 1;
    }

    cout << "Created UDP socket at: " << sock.address() << endl;

    string s, sret;
    while (getline(cin, s) && !s.empty()) {
        const size_t N = s.length();

        if (auto res = sock.send(s); res != N) {
            cerr << "Error writing to the UDP socket: " << res.error_message() << endl;
            break;
        }
        printf("send %s\n", s);

        // sret.resize(N);
        // if (auto res = sock.recv(&sret[0], N); res != N) {
        //     cerr << "Error reading from UDP socket: " << res.error_message() << endl;
        //     break;
        // }

        // cout << sret << endl;
    }

    return (!sock) ? 1 : 0;

    return 0;
}