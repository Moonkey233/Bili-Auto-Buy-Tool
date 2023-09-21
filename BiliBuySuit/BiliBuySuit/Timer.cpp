#include "Timer.h"

Timer::Timer(BuySuit* bs, int lt, int st, string port, string ta)
{
	try {
		_buySuit = bs;
		_predictTime = bs->_predictTime;
		_localTime = lt;
		_socketTime = st;
		strcpy_s(_port, port.c_str());
		_host = ta;
		this->_saleTime = bs->_saleTime;

		if (_saleTime - time(0) > 10 && Tools::isAdmin()) {
			long long t = clock();
			string json_str = "{\"Connection\":\"close\"}";
			Json::Reader reader;
			Json::Value headers;
			Json::Value* root;
			reader.parse(json_str, headers);

			string url = "https://app.bilibili.com/x/v2/splash/show";
			HttpRequests* httpRequests = new HttpRequests(url, "https");
			httpRequests->generateMsg("GET", url, Json::nullValue, Json::nullValue, "", true, 1024);
			httpRequests->connectHost();
			root = httpRequests->getJson(false);
			long long real_time = stoll((*root)["data"]["splash_request_id"].asString().substr(0, 13));
			delete httpRequests, root;
			httpRequests = nullptr;
			root = nullptr;
			Tools::setSysTime(real_time + 10);
			Tools::SetColorAndBackground(14, 0);
			cout << "本地时间已修改: " << real_time << endl;
			Tools::SetColorAndBackground(15, 0);
		}
	}
	catch (...) {
		Tools::errorPause("initTimer error");
	}
}

Timer::~Timer()
{

}

int Timer::waitLocalTime()
{
	try {
		Tools::SetColorAndBackground(14, 0);
		cout << "剩余抢购时间: " << to_string(_saleTime - time(0)) << "s" << endl;
		while ((int)time(0) + _localTime + 1 < _saleTime) {
			int sleep_time = (int)(_saleTime - time(0) - _localTime);
			cout << "本地计时器: 程序休眠 " << sleep_time << "s" << endl;
			this_thread::sleep_for(chrono::milliseconds(1000 * sleep_time));
		}
		Tools::SetColorAndBackground(15, 0);
		return 0;
	}
	catch (...) {
		Tools::errorPause("waitLocalTime error");
		return -1;
	}
}

int Timer::waitServerTime()
{
	try {
		if (_buySuit->_timerMethod == 3) {
			WSADATA wsadata{};
			WORD w_req = MAKEWORD(2, 2);
			if (WSAStartup(w_req, &wsadata) != 0) {
				Tools::errorPause("初始化套接字库失败");
			}

			addrinfo hints{};
			addrinfo* _result;
			memset(&hints, 0, sizeof(hints));
			hints.ai_family = AF_INET;
			hints.ai_socktype = SOCK_STREAM;
			hints.ai_protocol = IPPROTO_TCP;
			getaddrinfo(_host.c_str(), _port, &hints, &_result);

			SOCKET _timeSocket = INVALID_SOCKET;
			_timeSocket = socket(_result->ai_family, _result->ai_socktype, _result->ai_protocol);
			cout << "\nTimerSocket初始化成功" << endl;

			connect(_timeSocket, _result->ai_addr, sizeof(*_result->ai_addr));
			cout << _host << ":" << _port << " 时间服务端连接成功" << endl;

			string saleTime = to_string(_saleTime * 1000 - _predictTime);
			send(_timeSocket, saleTime.c_str(), (int)saleTime.length(), 0);
			cout << "已发送购买时间: " << saleTime << endl;

			while (true) {
				char buf[16] = {};
				recv(_timeSocket, buf, 16, 0);
				buf[strlen(buf)] = '\0';
				string msg = buf;
				if (msg == "0") {
					_buySuit->post();
					//cout << "main buy" << endl;
					break;
				}
				else if (msg == "-1") {
					Tools::errorPause("抢购已过时");
				}
				else if (msg == "2") {
					int sleepTime = 5000 - _socketTime * 1000 >= 0 ? 5000 - _socketTime * 1000 : 2000;
					this_thread::sleep_for(chrono::milliseconds(sleepTime));
					_buySuit->connectServer();
					continue;
				}
				else {
					continue;
				}
			}
		}
		else if (_buySuit->_timerMethod == 1 || _buySuit->_timerMethod == 2) {
			int thread_num = _buySuit->_timerMethod == 1 ? 36 : 1;
			thread thread_pool[36];
			SYSTEMTIME currentTime{};
			cout << _saleTime * 1000 << endl;
			while (time(0) + _socketTime < _saleTime) {
				GetLocalTime(&currentTime);
				cout << "\r" << (long long)(time(0) * 1000 + currentTime.wMilliseconds);
				this_thread::sleep_for(chrono::milliseconds(50));
				continue;
			}
			GetLocalTime(&currentTime);
			cout << "\r" << (long long)(time(0) * 1000 + currentTime.wMilliseconds) << endl;
			_buySuit->connectServer();
			bool flag = false;
			mutex mylock;
			for (int i = 0; i < thread_num; i++) {
				thread_pool[i] = thread(timeRequest, _saleTime * 1000 - _predictTime, ref(flag), ref(mylock), ref(_postTime));
			}
			Tools::SetColorAndBackground(2, 0);
			cout << "线程启动成功" << endl;
			while (true) {
				//cout << "";
				mylock.lock();
				if (flag) {
					_buySuit->post();
					//cout << "Main buy\n";
					mylock.unlock();
					break;
				}
				mylock.unlock();
			}
			for (int i = 0; i < thread_num; i++) {
				thread_pool[i].join();
			}
		}
		Tools::SetColorAndBackground(2, 0);
		return 0;
	}
	catch (...) {
		Tools::errorPause("waitServerTime error");
		return -1;
	}
}

void* Timer::timeRequest(long long t, bool &flag, mutex& mylock, long long &postTime) {
	try {
		string json_str = "{\"Connection\":\"keep-alive\"}";
		Json::Reader reader;
		Json::Value headers;
		Json::Value* root;
		reader.parse(json_str, headers);

		string url = "https://app.bilibili.com/x/v2/splash/show";
		HttpRequests* httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, Json::nullValue, Json::nullValue, "", false, 1024);
		httpRequests->connectHost();

		//long long t = sale_time * 1000;
		long long now_time = 0;

		for (int i = 0; i < 100; i++) {
			if (!flag) {
				root = httpRequests->getJson(false);
				now_time = stoll((*root)["data"]["splash_request_id"].asString().substr(0, 13));
				delete root;
				root = nullptr;
				//cout << now_time << endl;
				if (now_time > t) {
					mylock.lock();
					if (!flag) {
						cout << "触发时间戳: " << now_time << endl;
						postTime = now_time;
					}
					flag = true;
					mylock.unlock();
					break;
				}
			}
		}
		delete httpRequests;
		httpRequests = nullptr;
	}
	catch (...) {
		Tools::errorPause("timeReq error");
	}
}

int Timer::writeLog() {
	try {
		string fileName = "log_" + _name + "_" + Tools::stampTostandard(time(0), "%Y-%m-%d-%H-%M-%S") + ".txt";
		ofstream fout(fileName);
		if(_buySuit->_isNewHost)
			fout << "【新接口】" << "\r\n" << endl;
		else
			fout << "【老接口】" << "\r\n" << endl;
		fout << "延迟: " << _buySuit->_predictTime << " ms\r\n" << endl;
		fout << "抢购时间戳: " << _buySuit->_saleTime << "000\r\n" << endl;
		fout << "触发时间戳: " << _postTime << "\r\n" << endl;
		fout << "实际延迟: " << _buySuit->_saleTime * 1000 -_postTime << " ms\r\n" << endl;
		fout << "耗时: " << _buySuit->_costTime << " ms\r\n" << endl;
		int number = _ownNum > 0 ? _number + _ownNum - 1 : 0;
		fout << "编号区间: " << _number << " - " << number << "\r\n" << endl;
		fout << _buySuit->getRecv() << endl;
		fout.close();
		Tools::SetColorAndBackground(2, 0);
		cout << "文件已写入: " + fileName << endl;
		return 0;
	}
	catch (...) {
		Tools::errorPause("writeLog error");
	}
}

int Timer::reqOwnNumber() {
	try {
		string json_str = "{\"user-agent\": \"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.50\",\"referer\": \"https://www.bilibili.com/\",\"sec-fetch-site\": \"same-site\",\"sec-fetch-mode\": \"cors\",\"sec-fetch-dest\": \"empty\",\"sec-ch-ua-platform\": \"Android\",\"sec-ch-ua-mobile\": \"?1\",\"origin\": \"https://www.bilibili.com\",\"accept-language\": \"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\",\"accept\": \"application/json, text/plain, */*\",\"connection\":\"close\"}";
		Json::Reader reader;
		Json::Value headers;
		Json::Value cookies = _buySuit->getCookies();
		Json::Value* root;
		reader.parse(json_str, headers);
		string data = _buySuit->getData();

		string url = "https://api.bilibili.com/x/garb/user/asset";
		HttpRequests* httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, cookies, data, true, 4096);
		httpRequests->connectHost();

		root = httpRequests->getJson(true);
		_ownNum = (*root)["data"]["own_num"].asInt();
		_name = _buySuit->_saleName;
		if (_ownNum > 0) {
			_number = (*root)["data"]["fan"]["number"].asInt();
			Tools::SetColorAndBackground(11, 0);
			if (_ownNum > 1) {
				cout << "【" << _name << "】>>检测到购买编号区间: " << _number << " - " << _number + _ownNum - 1 << endl;
			} else {
				cout << "【" << _name << "】>>检测到购买编号: " << _number << endl;
			}
		} else {
			Tools::SetColorAndBackground(4, 0);
			cout << "未检测到购买编号" << endl;
		}
		cout << endl;

		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;
		return 0;
	}
	catch (...) {
		Tools::errorPause("reqOwnNumber error");
	}
}