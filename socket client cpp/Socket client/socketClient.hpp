#include <string.h>

class socketClient
{
private:
    char *clientIP;
    char *serverIP = "192.30.10.1";
    int serverPort = 70;
    int descriptor;
    struct sockaddr_in Server;
    int ServerLength = sizeof(Server);
    char *buffer;

public:
    socketClient(char *IP);
    void openClient();
    void closeSocket(char *option)
    char* receive();
    void send(char *clientIP, void *data);
    void changeclientIP(char *newIP);
    void changeserverPort(int p);
};

