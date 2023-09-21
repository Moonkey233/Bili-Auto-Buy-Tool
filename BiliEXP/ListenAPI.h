#ifndef _LISTENAPI_H_
#define _LISTENAPI_H_
#include <stdlib.h>
#include <string>
#include "HttpRequests.h"

using namespace std;

class ListenAPI
{
public:
	ListenAPI(int sleepTimeMS, int start, int end, string id, Json::Value cookies, int speedNum = 10);
	~ListenAPI();
	int startListen();

private:
	int _start;
	int _end;
	int _speedNum;
	int _sleepTimeMS;
	string _itemId;
	Json::Value _cookies;
};

#endif
