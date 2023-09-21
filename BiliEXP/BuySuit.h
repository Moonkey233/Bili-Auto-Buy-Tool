#ifndef _BUYSUIT_H_
#define _BUYSUIT_H_
#pragma warning(disable:4996)
#include <stdlib.h>
#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <ctime>
#include <thread>
#include "WinSock2.h"
#include "openssl/ssl.h"
#include "openssl/md5.h"
#include "HttpRequests.h"
#include "Tools.h"
#pragma comment(lib,"ws2_32.lib")
#pragma comment(lib,"libssl.lib")
#pragma comment(lib,"libcrypto.lib")

using namespace std;

class BuySuit
{
public:
	bool _isAutoBuy;
	int _expSTART;
	int _expEND;
	string _itemId;

	BuySuit(string bn = "1", string am = "-1", string ct = "", string fs = "shop", string from = "feed.card", string mp = "./message.txt", bool autoBuy = true);
	~BuySuit();
	int post();
	int connectServer();
	int generateMessage();
	int autoSetBuyNum(int true_number);
	Json::Value getCookies();
	int getSpeedNum();

private:
	SSL* _ssl;
	SSL_CTX* _ctx;
	addrinfo* _result;
	WSADATA _wsadata;
	SOCKET _serverSocket;
	stringstream _stream;
	char _rec[4097];
	char _sendData[4096];

	const char _port[16] = "https";
	const string _host = "api.live.bilibili.com";
	const SSL_METHOD* _meth = TLS_client_method();

	int _expNUM;
	int _saleBP;
	int _speedNUM;
	string _sessdata;
	string _biliJct;
	string _uid;
	string _ckmd5;
	string _sid;
	string _buvid;
	string _agent;
	string _eid;
	string _accessKey;
	string _appkey;
	string _csrf;
	string _statistics;
	string _buyNum;
	string _addMonth;
	string _couponToken;
	string _fSource;
	string _shopFrom;
	string _messagePath;

	int wsaInit();
	int socketInit();
	int sslInit();
	int showInfo();
	int inputInfo();
	int parseMessage();
	int findData(char* buf, string* key, string start, string end);
	string generateTraceID(long long sale_time);
	string urlEncode();
};

#endif // !_BUYSUIT_H_
