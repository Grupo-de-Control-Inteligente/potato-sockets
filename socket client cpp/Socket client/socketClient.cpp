#include "socketSClient.hpp"
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <iostream>

using namespace std;

//constructor de la clase socketClient

socketClient::socketClient(char *IP)
{
    changeclientIP(IP);

    this.descriptor = socket(AF_INET,SOCK_DGRAM,O);

    if (descriptor == -1)
    {
        cout << "Error creating socket\n" << endl;
    }
}

//abre el servicio del socket para enviar y recibir datos

void socketServer::openClient()
{

    this.Server.sin_family = AF_INET;
    this.Server.sin_port = this.serverPort;
    this.Server.sin_addr.s_addr = this.serverIP;

    struct sockaddr_in Address;
    Address.sin_family = AF_INET;
    Address.sin_port = 0;
    Address.sin_addr.s_addr = INADDR_ANY;

    if(bind(descriptor, (struct sockaddr *)&Address, sizeof(Address)) == -1)
    {
        cout << "Error while opening service\n" << endl;
    }
}

//con esta función mandamos datos al servidor

void socketServer::send(char *serverIP, char *data)
{
    strcpy(this.buffer, data);
    if(sendto(this.descriptor, (char *)&this.buffer, sizeof(this.buffer), 0, (struct sockaddr *)&this.Server, this.ServerLength) == -1)
    {
        cout << "Error sending data\n" << endl;
        this.buffer = NULL;
    }
}

//ponemos el cliente a recibir mensajes y guarda en una estructura la info del servidor

char* socketServer::receive()
{
    if(recvfrom(this.descriptor, (char *)&this.buffer, sizeof(this.buffer), 0, (struct sockaddr *)&this.Server, &this.ServerLength) == -1)
    {
        cout << "Error receiving data\n" << endl;
        return NULL;
    }
    else
    {
    this.Server.sin_family = AF_INET;
    this.Server.sin_port = this.serverPort;
    this.Server.sin_addr.s_addr = this.serverIP;
        return this.buffer;
    }
}

//cierra las comunicaciones en uno de los sentidos o totalmente

void socketClient::closeSocket(char *option)
{
    int mode;

    if(!strcmp(option, "receive"))
    {
        mode = 0;
    }
    else if (!strcmp(option, "send"))
    {
        mode = 1;
    }
    else
    {
        mode = 2;
    }

    shutdown(descriptor, mode);
}

//no se si necesaria, por si queremos cambiar la IP del servidor

void socketClient::changeclientIP(char *newIP)
{
    strcpy(this.clientIP, newIP);
}

//no se si necesaria, por si queremos cambiar el puerto por el que damos servicio

void socketClient::changeserverPort(int p)
{
    this.serverPort = p;
}

//destructor del objeto socketClient, puede que no sea necesario

socketClient::~socketClient()
{
    close(descriptor);
}

