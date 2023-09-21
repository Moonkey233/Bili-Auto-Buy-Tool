#ifndef _HTTPREQUEST_H_
#define _HTTPREQUEST_H_
#pragma warning(disable:4996)
#include <string>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <Ws2tcpip.h>
#include <WinSock2.h>
#include "json/json.h"
#include "openssl/ssl.h"
#include "openssl/md5.h"
#include "Tools.h"
#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib,"libssl.lib")
#pragma comment(lib,"libcrypto.lib")
#pragma comment(lib,"json_vc71_libmt.lib")

class HttpRequests
{
public:
	HttpRequests(std::string url, const char* servicePort = "");
	~HttpRequests();
	int connectHost();
	int setMsg(const char* message);
	int generateMsg(const char* method = "GET", std::string url = "", Json::Value headers = Json::nullValue, Json::Value cookies = Json::nullValue, std::string data = "", bool decode = true, unsigned short recvLen = 1024);
	//int generateMsg(const char* method = "GET", std::string url = "", Json::Value headers = Json::nullValue, std::string cookies = "", std::string data = "", bool decode = true, unsigned short recvLen = 1024);
	char* request(bool decode = true);
	static char* getBody(char* message);
	Json::Value* getJson(bool decode = true);

private:
	SSL* _ssl;
	SSL_CTX* _ctx;
	SOCKET _connectSocket;
	WORD _wVersionRequested;
	WSADATA _wsaData;
	addrinfo* _result;
	char _hostAddr[256];
	char _url[256];
	char _PORT[16];
	char _sendMessage[4096];
	char _sendData[2048];
	char _recvBuf[65537];
	unsigned short _recvLen;
	const SSL_METHOD* _meth = TLS_client_method();
};

#endif // !_HTTPREQUEST_H_
