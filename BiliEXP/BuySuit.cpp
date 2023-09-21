#include "BuySuit.h"

BuySuit::BuySuit(string bn, string am, string ct, string fs, string from, string mp, bool autoBuy)
{
	try {
		_buyNum = bn;
		_addMonth = am;
		_couponToken = ct;
		_fSource = fs;
		_shopFrom = from;
		_messagePath = mp;
		_isAutoBuy = autoBuy;
		wsaInit();
		socketInit();
		sslInit();
		parseMessage();
		showInfo();
		Tools::SetColorAndBackground(2, 0);
		cout << "\n>>初始化完成<<\n" << endl;
		Tools::SetColorAndBackground(15, 0);
	}
	catch (...) {
		Tools::errorPause("initBuysuit error");
	}
}

int BuySuit::connectServer()
{
	if (connect(_serverSocket, _result->ai_addr, sizeof(*_result->ai_addr)) < 0) {
		WSACleanup();
		Tools::errorPause("\nSocket连接失败");
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "\nSocket连接成功" << endl;
	}
	if (SSL_connect(_ssl) < 0) {
		WSACleanup();
		Tools::errorPause("SSL连接验证失败");
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "SSL连接验证成功" << endl;
	}
	return 0;
}

int BuySuit::post() {
	try {
		long long t = clock();
		SSL_write(_ssl, _sendData, (int)strlen(_sendData));
		cout << "报文发送成功" << endl;
		SSL_read(_ssl, _rec, 1);
		long long e = clock();
		SSL_read(_ssl, _rec + 1, 4096);
		cout << "报文接收成功\n" << endl;
		_rec[strlen(_rec)] = '\0';
		Tools::encodeToUTF8(_rec);
		Tools::SetColorAndBackground(15, 0);
		cout << _rec << endl;
		Tools::SetColorAndBackground(14, 0);
		cout << "\n>>抢购结束, 耗时: " << e - t << "ms" << endl;
		return 0;
	}
	catch (...) {
		Tools::errorPause("post error");
		return -1;
	}
}

int BuySuit::wsaInit()
{
	WORD w_req = MAKEWORD(2, 2);
	if (WSAStartup(w_req, &_wsadata) != 0) {
		Tools::SetColorAndBackground(4, 0);
		Tools::errorPause("初始化套接字库失败");
		Tools::SetColorAndBackground(15, 0);
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "初始化套接字库成功" << endl;
		Tools::SetColorAndBackground(15, 0);
	}
	if (LOBYTE(_wsadata.wVersion) != 2 || HIBYTE(_wsadata.wHighVersion) != 2) {
		Tools::SetColorAndBackground(4, 0);
		WSACleanup();
		Tools::errorPause("套接字库版本号不符");
		Tools::SetColorAndBackground(15, 0);
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "套接字库版本号正确" << endl;
		Tools::SetColorAndBackground(15, 0);
	}
	return 0;
}

string BuySuit::urlEncode()
{
	try {
		stringstream body;
		body << "access_key=" << _accessKey;
		body << "&appkey=" << _appkey;
		body << "&biz_extra=%7B%22add_month%22%3A" << _addMonth << "%2C%22coupon_token%22%3A%22%" << _couponToken << "22%2C%22m_source%22%3A%22%22%2C%22f_source%22%3A%22" << _fSource << "%22%2C%22from%22%3A%22" << _shopFrom << "%22%2C%22from_id%22%3A%22%22%7D";
		body << "&biz_id=" << _itemId;
		body << "&biz_source=1";
		body << "&context_id=0";
		body << "&context_type=102";
		body << "&csrf=" << _csrf;
		body << "&disable_rcmd=0";
		body << "&goods_id=195";
		body << "&goods_num=" << _buyNum;
		body << "&pay_bp=" << _saleBP * atoi(_buyNum.c_str());
		body << "&platform=android";
		body << "&statistics=" << _statistics;
		body << "&ts=" << to_string(time(0));

		string form_data = body.str();
		string app_sec = "560c52ccd288fed045859ed18bffd973";
		string form_data_sec = form_data + app_sec;
		unsigned char mdStr[33] = { 0 };
		MD5((const unsigned char*)form_data_sec.c_str(), form_data_sec.length(), mdStr);
		string encodedStr = string((const char*)mdStr);
		char buf[65] = { 0 };
		char tmp[3] = { 0 };
		for (int i = 0; i < 32; i++) {
			sprintf_s(tmp, "%02x", mdStr[i]);
			strcat_s(buf, tmp);
		}
		buf[32] = '\0';
		string encodedHexStr = string(buf);
		return form_data + "&sign=" + encodedHexStr;
	}
	catch (...) {
		Tools::errorPause("urlEncode error");
		return "";
	}
}

string BuySuit::generateTraceID(long long sale_time)
{
	try {
		string uuid = Tools::uuid(26);
		string s = Tools::intToHex(sale_time / 256);
		string traceID = uuid + s + ":" + uuid.substr(16) + s + ":0:0";
		return traceID;
	}
	catch (...) {
		Tools::errorPause("traceID error");
		return "";
	}
}

int BuySuit::socketInit()
{
	addrinfo hints{};
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;
	getaddrinfo(_host.c_str(), _port, &hints, &_result);
	_serverSocket = socket(_result->ai_family, _result->ai_socktype, _result->ai_protocol);

	if (_serverSocket == NULL) {
		Tools::SetColorAndBackground(4, 0);
		WSACleanup();
		Tools::errorPause("Socket初始化失败");
		Tools::SetColorAndBackground(15, 0);
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "Socket初始化成功" << endl;
		Tools::SetColorAndBackground(15, 0);
	}
	return 0;
}

int BuySuit::sslInit()
{
	SSLeay_add_ssl_algorithms();
	_ctx = SSL_CTX_new(_meth);
	if (_ctx == nullptr) {
		Tools::SetColorAndBackground(4, 0);
		WSACleanup();
		Tools::errorPause("SSL_CTX创建失败");
		Tools::SetColorAndBackground(15, 0);
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "SSL_CTX创建成功" << endl;
		Tools::SetColorAndBackground(15, 0);
	}
	_ssl = SSL_new(_ctx);
	if (_ssl == nullptr) {
		Tools::SetColorAndBackground(4, 0);
		WSACleanup();
		Tools::errorPause("SSL创建失败");
		Tools::SetColorAndBackground(15, 0);
	}
	else {
		Tools::SetColorAndBackground(2, 0);
		cout << "SSL创建成功" << endl;
		Tools::SetColorAndBackground(15, 0);
	}
	SSL_set_fd(_ssl, (int)_serverSocket);
	return 0;
}

int BuySuit::inputInfo() {
	try {
		string inputSTART, inputEND, inputNUM, expNUM, itemID, speedNUM;
		cout << "\n";
		//_expSTART = 11120;
		//_expEND = 12120;
		//_expNUM = 12121;
		//_expSTART = 11081;
		//_expEND = 11081;
		//_expNUM = 11093;
		//_buyNum = "1";
		Tools::SetColorAndBackground(11, 0);
		cout << "文件中item_id: " << _itemId << endl;
		while (true)
		{
			Tools::SetColorAndBackground(11, 0);
			cout << "请输入item_id: ";
			cin >> itemID;
			if (atoi(itemID.c_str()) != 0) {
				_itemId = itemID;
				break;
			}
			else
			{
				Tools::errorPause("输入格式错误, 请输入数字");
				continue;
			}
		}
		while (true)
		{
			Tools::SetColorAndBackground(11, 0);
			cout << "请输入加速区间: ";
			cin >> speedNUM;
			if (atoi(speedNUM.c_str()) != 0) {
				_speedNUM = atoi(speedNUM.c_str());
				break;
			}
			else
			{
				Tools::errorPause("输入格式错误, 请输入数字");
				continue;
			}
		}
		while (true)
		{
			Tools::SetColorAndBackground(11, 0);
			cout << "请输入预期播报区间较小值: ";
			cin >> inputSTART;
			if (atoi(inputSTART.c_str()) != 0) {
				_expSTART = atoi(inputSTART.c_str());
				break;
			}
			else
			{
				Tools::errorPause("输入格式错误, 请输入数字");
				continue;
			}
		}
		while (true)
		{
			Tools::SetColorAndBackground(11, 0);
			cout << "请输入预期播报区间较大值: ";
			cin >> inputEND;
			if (atoi(inputEND.c_str()) != 0 && atoi(inputEND.c_str()) >= _expSTART) {
				_expEND = atoi(inputEND.c_str());
				break;
			}
			else
			{
				Tools::errorPause("输入格式错误, 请输入数字且大于等于播报较小值");
				continue;
			}
		}
		while (true)
		{
			Tools::SetColorAndBackground(11, 0);
			cout << "请输入最大抢购数量: ";
			cin >> inputNUM;
			if (atoi(inputNUM.c_str()) != 0) {
				_buyNum = inputNUM;
				break;
			}
			else
			{
				Tools::errorPause("输入格式错误, 请输入数字");
				continue;
			}
		}
		while (true)
		{
			Tools::SetColorAndBackground(11, 0);
			cout << "请输入预期编号: ";
			cin >> expNUM;
			if (atoi(expNUM.c_str()) != 0 && _expEND + 1 <= atoi(expNUM.c_str()) && atoi(expNUM.c_str()) >= _expSTART + atoi(_buyNum.c_str())) {
				_expNUM = atoi(expNUM.c_str());
				break;
			}
			else
			{
				Tools::errorPause("输入格式错误, 请输入数字且大于等于播报较大值+1, 大于等于较小值+最大购买数");
				continue;
			}
		}
		return 0;
	}
	catch (...) {
		Tools::errorPause("input error");
		return -1;
	}
}

int BuySuit::parseMessage()
{
	try {
		char buffer[1024]{};
		ifstream in(_messagePath.c_str(), ios::in);
		if (!in.is_open()) {
			WSACleanup();
			Tools::errorPause("文件打开失败");
		}
		while (!in.eof()) {
			in.getline(buffer, 1024);
			findData(buffer, &_itemId, "item_id=", "&");
			findData(buffer, &_accessKey, "access_key=", "&");
			findData(buffer, &_appkey, "appkey=", "&");
			findData(buffer, &_csrf, "csrf=", "&");
			findData(buffer, &_statistics, "statistics=", "&");
			findData(buffer, &_sessdata, "SESSDATA=", ";");
			findData(buffer, &_biliJct, "bili_jct=", ";");
			findData(buffer, &_uid, "DedeUserID=", ";");
			findData(buffer, &_ckmd5, "DedeUserID__ckMd5=", ";");
			findData(buffer, &_sid, "sid=", ";");
			findData(buffer, &_buvid, "Buvid=", "NULL");
			findData(buffer, &_agent, "User-Agent: ", "NULL");
			findData(buffer, &_eid, "x-bili-aurora-eid: ", "NULL");
		}
		in.close();
		if (_itemId == "" || _accessKey == "" || _appkey == "" || _csrf == "" || _statistics == "" || _sessdata == "" || _biliJct == "" || _uid == "" || _ckmd5 == "" || _sid == "" || _buvid == "" || _agent == "" || _eid == "") {
			Tools::errorPause("文件信息缺失");
		}

		inputInfo();

		return 0;
	}
	catch (...) {
		Tools::errorPause("parseMsg error");
		return -1;
	}
}

int BuySuit::generateMessage() {
	try {
		string messageBody = urlEncode();
		string length = to_string(messageBody.length());
		_stream << "POST https://api.live.bilibili.com/xlive/revenue/v2/order/createOrder HTTP/1.1\r\n";
		_stream << "Host: api.live.bilibili.com\r\n";
		_stream << "Connection: keep-alive\r\n";
		_stream << "Content-Length: " << length << "\r\n";
		_stream << "native_api_from: h5\r\n";
		_stream << "Cookie: SESSDATA=" << _sessdata << "; bili_jct=" << _biliJct << "; DedeUserID=" << _uid << "; DedeUserID__ckMd5=" << _ckmd5 << "; sid=" << _sid << "; Buvid=" << _buvid << "\r\n";
		_stream << "buvid: " << _buvid << "\r\n";
		_stream << "Accept: application/json, text/plain, */*\r\n";
		_stream << "Referer: https://www.bilibili.com/h5/mall/suit/detail?navhide=1" << "&from=" << _shopFrom << "&id=" << _itemId << "&f_source=shop" << "&native.theme=1\r\n";
		_stream << "Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n";
		_stream << "env: prod\r\n";
		_stream << "APP-KEY: android64\r\n";
		_stream << "User-Agent: " << _agent << "\r\n";
		_stream << "x-bili-trace-id: " << generateTraceID(time(0)) << "\r\n";
		_stream << "x-bili-aurora-eid: " << _eid << "\r\n";
		_stream << "x-bili-mid: " << _uid << "\r\n";
		_stream << "x-bili-aurora-zone: \r\n";
		_stream << "bili-http-engine: cronet\r\n";
		//_stream << "Accept-Encoding: gzip, deflate, br\r\n\r\n";
		_stream << "Accept-Encoding: gzip\r\n\r\n";
		_stream << messageBody;
		memset(_sendData, '\0', sizeof(_sendData));
		string s = _stream.str();
		strcpy_s(_sendData, s.c_str());

		//cout << _sendData << endl;
		//system("pause");

		return 0;
	}
	catch (...) {
		Tools::errorPause("generateMsg error");
		return -1;
	}
}

int BuySuit::autoSetBuyNum(int true_number) {
	if (_isAutoBuy && ((_expNUM - true_number) < atoi(_buyNum.c_str()))) {
		_buyNum = to_string((_expNUM - true_number));
	}
	return 0;
}

Json::Value BuySuit::getCookies() {
	Json::Value cookies;
	cookies["SESSDATA"] = _sessdata;
	cookies["bili_jct"] = _biliJct;
	cookies["DedeUserID"] = _uid;
	cookies["DedeUserID__ckMd5"] = _ckmd5;
	cookies["sid"] = _sid;
	cookies["Buvid"] = _buvid;
	return cookies;
}

int BuySuit::findData(char* buf, string* key, string start, string end)
{
	try {
		if (*key == "") {
			string temp = Tools::findValue(buf, start, end);
			if (temp != "") {
				*key = temp;
			}
		}
		return 0;
	}
	catch (...) {
		Tools::errorPause("findData error");
		return -1;
	}
}

int BuySuit::showInfo() {
	try {
		string json_str = "{\"user-agent\": \"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.50\",\"referer\": \"https://www.bilibili.com/\",\"sec-fetch-site\": \"same-site\",\"sec-fetch-mode\": \"cors\",\"sec-fetch-dest\": \"empty\",\"sec-ch-ua-platform\": \"Android\",\"sec-ch-ua-mobile\": \"?1\",\"origin\": \"https://www.bilibili.com\",\"accept-language\": \"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\",\"accept\": \"application/json, text/plain, */*\",\"connection\":\"close\"}";
		Json::Reader reader;
		Json::Value headers;
		Json::Value* root;
		reader.parse(json_str, headers);

		string url = "https://api.bilibili.com/x/space/acc/info?mid=" + _uid;
		HttpRequests* httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, getCookies(), "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		string name = (*root)["data"]["name"].asString();
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		url = "https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf=" + _csrf + "&from=feed.card&item_id=" + _itemId + "&part=suit";
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, getCookies(), "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		_saleBP = stol((*root)["data"]["properties"]["sale_bp_forever_raw"].asString()) * 10;
		string sale_name = (*root)["data"]["name"].asString();
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		url = "https://api.bilibili.com/x/garb/rank/fan/recent?item_id=" + _itemId;
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, getCookies(), "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		int i = 0;
		int now_num = (*root)["data"]["rank"][i]["number"].asInt();
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		url = "https://api.bilibili.com/x/garb/user/wallet";
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, getCookies(), "", false, 1024);
		httpRequests->connectHost();
		root = httpRequests->getJson(false);
		int bcoin = (int)((*root)["data"]["bcoin_balance"].asDouble() * 1000 + 0.5);
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		system("cls");
		Tools::SetColorAndBackground(11, 0);
		cout << "用户名: " << name << "\n装扮名: " << sale_name << "\n原价单价(1000倍): " << _saleBP << "\nB币余额(1000倍): " << bcoin << endl;
		cout << "item_id: " << _itemId << "\n最大购买数量: " << _buyNum << endl;
		cout << "预期编号: " << _expNUM << endl;
		cout << "触发播报区间: " << _expSTART << " --- " << _expEND << endl;
		cout << "当前播报: " << now_num << "\n剩余间隔: " << _expSTART - now_num << "\n加速区间: " << _speedNUM << endl;
		if (_isAutoBuy) {
			cout << "isAutoBuy: TURE" << endl;
		}
		else {
			cout << "isAutoBuy: FLASE" << endl;
		}
		Tools::SetColorAndBackground(15, 0);

		cout << "\n请按下任意键确认..." << endl;
		system("pause");

		return 0;
	}
	catch (...) {
		Tools::errorPause("showInfo error");
		return -1;
	}
}

int BuySuit::getSpeedNum() {
	return _speedNUM;
}

BuySuit::~BuySuit()
{
	SSL_shutdown(_ssl);
	SSL_free(_ssl);
	SSL_CTX_free(_ctx);
	closesocket(_serverSocket);
	WSACleanup();
}