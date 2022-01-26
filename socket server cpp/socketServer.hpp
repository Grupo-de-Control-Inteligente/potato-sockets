#include <string.h>

class socketServer
{
private:
    char *serverIP = "192.30.10.1";
    int port = 70;
    int descriptor;
    struct sockaddr_in Client;
    int ClientLength = sizeof(Client);
    char *buffer;

public:
    socketServer();
    void openServer();
    void closeSocket(char *option)
    char* receive();
    void send(char *clientIP, void *data);
    void changeserverIP(char *newIP);
    void changeport(int p);
};
