#ifndef _REQUEST_H_
#define _REQUEST_H_
#pragma warning(disable:4996)
#include <iostream>
#include <WinSock2.h>
#include <stdlib.h>
#include <string>
#include <atlstr.h>
#include <sstream>
#include <algorithm>
#include "Color.h"
#include <openssl/err.h>
#include <openssl/ssl.h>
#include <openssl/md5.h>
#include <ctime>
#include <thread>
#include <json/json.h>
#pragma comment(lib,"ws2_32.lib")
#pragma comment(lib,"libssl.lib")
#pragma comment(lib,"libcrypto.lib")
#pragma comment(lib,"json_vc71_libmt.lib")

using namespace std;

class Request
{
public:
	char* get(bool decode = false);
	Request(string url, Json::Value headers = Json::nullValue, string cookies = "");
	~Request();

private:
	SOCKET req_socket = 0;
	hostent* ip = nullptr;
	sockaddr_in sin{};
	WSADATA wsadata;
	unsigned short port = 443;
	const SSL_METHOD* meth = TLSv1_2_client_method();
	SSL_CTX* ctx = nullptr;
	SSL* ssl = nullptr;
	char sendData[4096];
	char rec[51200] = {};
	char buf[51200] = {};
	char ch = {};
	int sendLength = 0;
	string replaceStr(string s, string old_str, string new_str = "");
};

#endif