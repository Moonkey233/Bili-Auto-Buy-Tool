#ifndef _TIMER_H_
#define _TIMER_H_
#include <stdlib.h>
#include <string>
#include <thread>
#include <mutex>
#include <iostream>
#include <WinSock2.h>
#include "BuySuit.h"
#include "HttpRequests.h"
#include "Tools.h"
#pragma comment(lib,"ws2_32.lib")

using namespace std;

class Timer
{
public:
	Timer(BuySuit *bs, int lt = 20, int st = 3, string port = "23333", string ta = "Moonkey233.top");
	~Timer();
	int waitLocalTime();
	int waitServerTime();

private:
	long long _saleTime;
	int _localTime;
	int _socketTime;
	int _predictTime;
	char _port[16];
	string _host;
	BuySuit* _buySuit;
	static void* timeRequest(long long sale_time, bool &flag, mutex &mylock);
};

#endif // !_TIMER_H_
