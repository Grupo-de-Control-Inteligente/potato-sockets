#include "socket_S.hpp"
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <iostream>

using namespace std;

//constructor de la clase socketServer

socketServer::socketServer()
{
    this.descriptor = socket(AF_INET,SOCK_DGRAM,O);

    if (descriptor == -1)
    {
        cout << "Error creating socket\n" << endl;
    }
}

//abre el servicio para enviar y recibir datos

void socketServer::openServer()
{
    struct sockaddr_in Address;
    Address.sin_family = AF_INET;
    Address.sin_port = this.port;
    Address.sin_addr.s_addr = INADDR_ANY;

    if(bind(descriptor, (struct sockaddr *)&Address, sizeof(Address)) == -1)
    {
        cout << "Error while opening service\n" << endl;
    }
}

//cierra las comunicaciones en uno de los sentidos o totalmente

void closeSocket(char *option)
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

//ponemos el servidor a recibir mensajes y guarda en una estructura la info del cliente que envía

char* socketServer::receive()
{
    if(recvfrom(this.descriptor, (char *)&this.buffer, sizeof(this.buffer), 0, (struct sockaddr *)&Client, &ClienLength) == -1)
    {
        cout << "Error receiving data\n" << endl;
        return NULL;
    }
    else
    {
        return this.buffer;
    }
}

//con esta función mandamos datos al cliente que queramos

void socketServer::send(char *clientIP, char *data)
{
    strcpy(this.buffer, data);
    if(sendto(Descriptor, (char *)&buffer, sizeof(buffer), 0, (struct sockaddr *)&Client, ClientLength) == -1)
    {
        cout << "Error sending data\n" << endl;
        this.buffer = NULL;
    }
}

//no se si necesaria, por si queremos cambiar la IP del servidor

void changeserverIP(char *newIP)
{
    strcpy(this.serverIP, newIP);
}

//no se si necesaria, por si queremos cambiar el puerto por el que damos servicio

void changeport(int p)
{
    this.port = p;
}

//destructor del objeto socketServer, puede que no sea necesario

socketServer::~socketServer()
{
    close(descriptor);
}
