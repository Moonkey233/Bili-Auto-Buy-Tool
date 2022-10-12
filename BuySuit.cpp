#include "BuySuit.h"

BuySuit::BuySuit(string bn, string am, string ct, string fs, string from, string st, string mp, bool isSplit, int pt)
{
	try {
		Tools::SetColorAndBackground(14, 0);
		cout << ">>建议提前修改本地时间\n" << endl;
		Tools::SetColorAndBackground(15, 0);
		_buyNum = bn;
		_addMonth = am;
		_couponToken = ct;
		_fSource = fs;
		_shopFrom = from;
		strcpy_s(_standardTime, st.c_str());
		_messagePath = mp;
		_isSplitMsg = isSplit;
		_predictTime = pt;
		wsaInit();
		socketInit();
		sslInit();
		_saleTime = Tools::standardToStamp(_standardTime);
		parseMessage();
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
	} else {
		Tools::SetColorAndBackground(2, 0);
		cout << "\nSocket连接成功" << endl;
	}
	if (SSL_connect(_ssl) < 0) {
		WSACleanup();
		Tools::errorPause("SSL连接验证失败");
	} else {
		Tools::SetColorAndBackground(2, 0);
		cout << "SSL连接验证成功" << endl;
	}

	if (_isSplitMsg) {
		SSL_write(_ssl, _sendHeader, (int)strlen(_sendHeader));
		Tools::SetColorAndBackground(2, 0);
		cout << "发送不完整报文" << endl;
	}
	return 0;
}

int BuySuit::post(){
	try {
		long long t = clock();
		if (_isSplitMsg) {
			SSL_write(_ssl, _sendBody, (int)strlen(_sendBody));
		}
		else {
			SSL_write(_ssl, _sendData, (int)strlen(_sendData));
		}
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
		body << "&add_month=" << _addMonth;
		body << "&appkey=" << _appkey;
		body << "&buy_num=" << _buyNum;
		body << "&coupon_token=" << _couponToken;
		body << "&csrf=" << _csrf;
		body << "&currency=bp";
		body << "&disable_rcmd=0";
		body << "&f_source=" << _fSource;
		body << "&from=" << _shopFrom;
		body << "&item_id=" << _itemId;
		body << "&platform=android";
		body << "&statistics=" << _statistics;
		body << "&ts=" << to_string(_saleTime);

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

		setTimer();
		setMethod();

		string messageBody = urlEncode();
		string length = to_string(messageBody.length());

		_stream << "POST https://api.bilibili.com/x/garb/v2/trade/create HTTP/1.1\r\n";
		_stream << "Host: api.bilibili.com\r\n";
		_stream << "Connection: keep-alive\r\n";
		_stream << "Content-Length: " << length << "\r\n";
		_stream << "native_api_from: h5\r\n";
		_stream << "Cookie: SESSDATA=" << _sessdata << "; bili_jct=" << _biliJct << "; DedeUserID=" << _uid << "; DedeUserID__ckMd5=" << _ckmd5 << "; sid=" << _sid << "; Buvid=" << _buvid << "\r\n";
		_stream << "Accept: application/json, text/plain, */*\r\n";
		_stream << "Referer: https://www.bilibili.com/h5/mall/suit/detail?id=" << _itemId << "&navhide=1&f_source=shop&from=feed.card\r\n";
		_stream << "Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n";
		_stream << "env: prod\r\n";
		_stream << "APP-KEY: android64\r\n";
		_stream << "User-Agent: " << _agent << "\r\n";
		_stream << "x-bili-trace-id: " << generateTraceID(_saleTime) << "\r\n";
		_stream << "x-bili-aurora-eid: " << _eid << "\r\n";
		_stream << "x-bili-mid: " << _uid << "\r\n";
		_stream << "x-bili-aurora-zone: \r\n";
		_stream << "bili-bridge-engine: cronet\r\n";
		_stream << "Accept-Encoding: gzip, deflate, br\r\n\r\n";
		_stream << messageBody;

		memset(_sendData, '\0', sizeof(_sendData));
		memset(_sendHeader, '\0', sizeof(_sendHeader));
		memset(_sendBody, '\0', sizeof(_sendBody));

		string s = _stream.str();
		strcpy_s(_sendData, s.c_str());

		strcpy_s(_sendHeader, _sendData);
		_sendHeader[strlen(_sendHeader) - 1] = '\0';
		_sendBody[0] = _sendData[strlen(_sendData) - 1];
		_sendBody[1] = '\0';
		return 0;
	}
	catch (...) {
		Tools::errorPause("parseMsg error");
		return -1;
	}
}

int BuySuit::findData(char *buf, string *key, string start, string end)
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

int BuySuit::setTimer() {
	try {
		Tools::SetColorAndBackground(14, 0);
		cout << "\n[1]本地多线程计时(默认); [2]本地单线程计时; [3]服务器代理计时(安全)\n";
		Tools::SetColorAndBackground(9, 0);
		cout << "请输入选择数字: ";
		Tools::SetColorAndBackground(15, 0);
		char ch = getchar();
		if (ch == '2') {
			_timerMethod = 2;
		}
		else if (ch == '3') {
			_timerMethod = 3;
		}
		else {
			_timerMethod = 1;
		}
		if (ch != '\n') {
			while (getchar() != '\n');
		}
		return 0;
	}
	catch (...) {
		Tools::errorPause("setTimer error");
		return -1;
	}
}

int BuySuit::setMethod() {
	try {
		string json_str = "{\"user-agent\": \"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.50\",\"referer\": \"https://www.bilibili.com/\",\"sec-fetch-site\": \"same-site\",\"sec-fetch-mode\": \"cors\",\"sec-fetch-dest\": \"empty\",\"sec-ch-ua-platform\": \"Android\",\"sec-ch-ua-mobile\": \"?1\",\"origin\": \"https://www.bilibili.com\",\"accept-language\": \"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\",\"accept\": \"application/json, text/plain, */*\",\"connection\":\"close\"}";
		Json::Reader reader;
		Json::Value headers;
		Json::Value cookies;
		Json::Value* root;
		reader.parse(json_str, headers);

		cookies["SESSDATA"] = _sessdata;
		cookies["bili_jct"] = _biliJct;
		cookies["DedeUserID"] = _uid;
		cookies["DedeUserID__ckMd5"] = _ckmd5;
		cookies["sid"] = _sid;
		cookies["Buvid"] = _buvid;

		string url = "https://api.bilibili.com/x/space/acc/info?mid=" + _uid;
		HttpRequests* httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, cookies, "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		delete httpRequests;

		string name = (*root)["data"]["name"].asString();

		url = "https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf=" + _csrf + "&from=feed.card&item_id=" + _itemId + "&part=suit";
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, cookies, "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		delete httpRequests;

		long long begin_time = stoll((*root)["data"]["properties"]["sale_time_begin"].asString());
		string sale_name = (*root)["data"]["name"].asString();


		Tools::SetColorAndBackground(2, 0);
		cout << "\n当前设置抢购时间: " << Tools::stampTostandard(_saleTime) << "\n已检测到开售时间: " << Tools::stampTostandard(begin_time) << endl;
		Tools::SetColorAndBackground(14, 0);
		cout << "\n[1]修改为预售时间(默认); [2]15秒后购买10套EveOneCat2; [3]下个整点购买10套EveOneCat2; [4]保持设置\n";
		Tools::SetColorAndBackground(9, 0);
		cout << "请输入选择数字: ";
		Tools::SetColorAndBackground(15, 0);
		char ch = getchar();
		if (ch == '2') {
			_itemId = "32296";
			_buyNum = "10";
			_saleTime = time(0) + 15;
			sale_name = "EveOneCat2";
			Tools::SetColorAndBackground(14, 0);
			cout << "15秒后将发送10套EveOneCat2购买请求, 请确保账户余额小于590" << endl;
			Tools::SetColorAndBackground(15, 0);
			this_thread::sleep_for(chrono::milliseconds(2000));
		}
		else if (ch == '3') {
			_itemId = "32296";
			_buyNum = "10";
			_saleTime = (((long long)time(0) + 5) / 3600 + 1) * 3600;
			sale_name = "EveOneCat2";
			Tools::SetColorAndBackground(14, 0);
			cout << "下个整点将发送10套EveOneCat2购买请求, 请确保账户余额小于590" << endl;
			Tools::SetColorAndBackground(15, 0);
			this_thread::sleep_for(chrono::milliseconds(2000));
		}
		else {
			if (ch != '4')
				_saleTime = begin_time;
		}
		if (ch != '\n') {
			while (getchar() != '\n');
		}

		if (_saleTime + 3 < time(0)) {
			WSACleanup();
			Tools::errorPause("\n抢购已过时");
		}
		system("cls");
		Tools::SetColorAndBackground(11, 0);
		cout << "抢购时间: " << Tools::stampTostandard(_saleTime) << endl;
		cout << "用户名: " << name << "\n装扮名: " << sale_name << endl;
		cout << "item_id: " << _itemId << "\n购买数量: " << _buyNum << "\nPredict_time: " << _predictTime << "ms" << endl;
		if (_isSplitMsg) {
			cout << "isSplitMsg: " << "TRUE" << endl;
		}
		else
		{
			cout << "isSplitMsg: " << "FALSE" << endl;
		}
		Tools::SetColorAndBackground(15, 0);
		return 0;
	}
	catch (...) {
		Tools::errorPause("setMothod error");
		return -1;
	}
}

BuySuit::~BuySuit()
{
	SSL_shutdown(_ssl);
	SSL_free(_ssl);
	SSL_CTX_free(_ctx);
	closesocket(_serverSocket);
	WSACleanup();
}