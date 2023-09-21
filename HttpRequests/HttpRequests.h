#ifndef _HTTPREQUEST_H_
#define _HTTPREQUEST_H_
#include <string>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <malloc.h>
#include <Ws2tcpip.h>
#include <WinSock2.h>
#include "json/json.h"
#include "openssl/ssl.h"
#include "openssl/md5.h"
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
	int generateMsg(const char* method = "GET", std::string url = "", Json::Value headers = Json::nullValue, Json::Value cookies = Json::nullValue, std::string data = "", bool decode = true, unsigned short recvLen = 4096);
	int generateMsg(const char* method = "GET", std::string url = "", Json::Value headers = Json::nullValue, std::string cookies = "", std::string data = "", bool decode = true, unsigned short recvLen = 4096);
	char* request(bool decode = true);
	static char* getBody(char* message);
	Json::Value* getJson(bool decode = true);

private:
	WORD _wVersionRequested;
	WSADATA _wsaData;
	addrinfo *_result;
	char _hostAddr[256];
	char _url[256];
	char _PORT[16];
	SOCKET _connectSocket;
	const SSL_METHOD* _meth = TLS_client_method();
	SSL_CTX* _ctx;
	SSL* _ssl;
	char _sendMessage[4096]{};
	char _sendData[2048]{};
	char _recvBuf[65537]{};
	unsigned short _recvLen;
	bool _isSSL;

	std::string replaceStrAll(std::string s, std::string old_str, std::string new_str);
	int encode(char* text);
};

#endif // !_HTTPREQUEST_H_
