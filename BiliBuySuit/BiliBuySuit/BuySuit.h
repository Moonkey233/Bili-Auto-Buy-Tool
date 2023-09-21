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
	int _costTime;
	int _predictTime;
	int _timerMethod;
	long long _saleTime;
	char _standardTime[32];
	bool _isNewHost;
	string _saleName;
	
	BuySuit(string host = "api.live.bilibili.com", string bn = "1", string am = "-1", string ct = "", string fs = "shop", string from = "feed.card", string st = "2022:10:01 19:00:00", string mp = "./message.txt", bool isSplit = false, int pt = 0, bool isAndroid = true);
	~BuySuit();
	int post();
	char* getRecv();
	int setTimer();
	int setMethod();
	int connectServer();
	string getData();
	Json::Value getCookies();
	
private:
	SSL* _ssl;
	SSL_CTX* _ctx;
	addrinfo* _result;
	WSADATA _wsadata;
	SOCKET _serverSocket;
	stringstream _stream;
	char _rec[4097];
	char _sendData[4096];
	char _sendHeader[4096];
	char _sendBody[2];
	bool _isSplitMsg;
	bool _isAndroid;

	const char _port[16] = "https";
	 //string _host = "api.bilibili.com";
	string _host = "api.live.bilibili.com";
	const SSL_METHOD* _meth = TLS_client_method();

	string _itemId;
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
	int _saleBP;

	int wsaInit();
	int socketInit();
	int sslInit();
	int parseMessage();
	int findData(char* buf, string *key, string start, string end);
	string generateTraceID(long long sale_time);
	string urlEncode();
	string getSign(string form_data);
};

#endif // !_BUYSUIT_H_
