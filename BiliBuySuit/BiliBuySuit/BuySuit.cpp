#include "BuySuit.h"

BuySuit::BuySuit(string host, string bn, string am, string ct, string fs, string from, string st, string mp, bool isSplit, int pt, bool isAndroid)
{
	try {
		Tools::SetColorAndBackground(14, 0);
		//cout << ">>建议提前修改本地时间\n" << endl;
		Tools::SetColorAndBackground(15, 0);
		_host = host;
		_buyNum = bn;
		_addMonth = am;
		_couponToken = ct;
		_fSource = fs;
		_shopFrom = from;
		strcpy_s(_standardTime, st.c_str());
		_messagePath = mp;
		_isSplitMsg = isSplit;
		_predictTime = pt;
		_isAndroid = isAndroid;
		wsaInit();
		_saleTime = Tools::standardToStamp(_standardTime);
		parseMessage();
		//socketInit();
		//sslInit();
		//Tools::SetColorAndBackground(2, 0);
		//cout << "\n>>初始化完成<<\n" << endl;
		//Tools::SetColorAndBackground(15, 0);
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
		_costTime = e - t;
		cout << "\n>>抢购结束, 耗时: " << _costTime << "ms" << endl;
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
		if (_isAndroid) {
			if (!_isNewHost) {
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
				body << "&from_id=";
				body << "&item_id=" << _itemId;
				body << "&m_source=";
				body << "&platform=android";
				body << "&statistics=" << _statistics;
				body << "&ts=" << to_string(_saleTime);
			} else {
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
				body << "&pay_bp=" << _saleBP;
				body << "&platform=android";
				body << "&statistics=" << _statistics;
				body << "&ts=" << to_string(_saleTime);
			}
		} else {
			body << "csrf=" << _csrf;
			body << "&ts=" << to_string(_saleTime);
			body << "&item_id=" << _itemId;
			body << "&platform=ios";
			body << "&currency=bp";
			body << "&add_month=" << _addMonth;
			body << "&buy_num=" << _buyNum;
			body << "&coupon_token=" << _couponToken;
			body << "&m_source=";
			body << "&f_source=" << _fSource;
			body << "&from=" << _shopFrom;
			body << "&from_id=";
			body << "&appkey=" << "27eb53fc9058f8c3";
			body << "&access_key=" << _accessKey;
			//body << "csrf=d002ded9ec32220d319ef409720f8b33&ts=1665588564&item_id=38741&platform=ios&currency=bp&add_month=-1&buy_num=1&coupon_token=&m_source=&f_source=shop&from=feed.card&from_id=&appkey=fb2c5b71e05297d0&access_key=c62c756d5d8189677865826a4251a3a1";
		}

		return getSign(body.str());
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
			if (_isAndroid) {
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
			} else {
				findData(buffer, &_itemId, "item_id=", "&");
				findData(buffer, &_accessKey, "access_key=", "&");
				findData(buffer, &_appkey, "appkey=", "&");
				findData(buffer, &_csrf, "csrf=", "&");
				findData(buffer, &_sessdata, "SESSDATA=", ";");
				findData(buffer, &_biliJct, "bili_jct=", ";");
				findData(buffer, &_uid, "DedeUserID=", ";");
				findData(buffer, &_ckmd5, "DedeUserID__ckMd5=", ";");
				findData(buffer, &_sid, "sid=", "NULL");
				findData(buffer, &_agent, "User-Agent: ", "NULL");
			}
		}
		in.close();

		//_itemId = "39636";
		//_accessKey = "e5c1ee028de3452ba1d533ad82e1e5a1";
		//_appkey = "1d8b6e7d45233436";
		//_csrf = "76f6c5e93f63347ebbc27b0e92decdd5";
		//_statistics = "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%227.0.0%22%2C%22abtest%22%3A%22%22%7D";
		//_sessdata = "795d6a55%2C1682758498%2C96fd98a1";
		//_biliJct = "76f6c5e93f63347ebbc27b0e92decdd5";
		//_uid = "1295520313";
		//_ckmd5 = "47e201edb1481515";
		//_sid = "nd41mej2";
		//_buvid = "XY0950501D960988398A7554196528B1DE9E4";
		//_agent = "Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 os/android model/MI 8 SE build/7000400 osVer/10 sdkInt/29 network/2 BiliApp/7000400 mobi_app/android channel/xiaomi Buvid/XY0950501D960988398A7554196528B1DE9E4 sessionID/1153709d innerVer/7000410 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 7.0.0 os/android model/MI 8 SE mobi_app/android build/7000400 channel/xiaomi innerVer/7000410 osVer/10 network/2";
		//_eid = "UFYIQ1QGBlIGXw==";

		//_itemId = "39636";
		//_accessKey = "f87309bfd8a1bbc6e05fb0b4b1fc63a1";
		//_appkey = "1d8b6e7d45233436";
		//_csrf = "c6188e36adf5e0a204347440cf0ac274";
		//_statistics = "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%227.0.0%22%2C%22abtest%22%3A%22%22%7D";
		//_sessdata = "b9381b6b%2C1682593705%2C550865a1";
		//_biliJct = "c6188e36adf5e0a204347440cf0ac274";
		//_uid = "86501805";
		//_ckmd5 = "1ee0f49081851542";
		//_sid = "nd41mej2";
		//_buvid = "XY0950501D960988398A7554196528B1DE9E4";
		//_agent = "Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 os/android model/MI 8 SE build/7000400 osVer/10 sdkInt/29 network/2 BiliApp/7000400 mobi_app/android channel/xiaomi Buvid/XY0950501D960988398A7554196528B1DE9E4 sessionID/1153709d innerVer/7000410 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 7.0.0 os/android model/MI 8 SE mobi_app/android build/7000400 channel/xiaomi innerVer/7000410 osVer/10 network/2";
		//_eid = "WVIERlAMBlQ=";

		if (_isAndroid) {
			if (_itemId == "" || _accessKey == "" || _appkey == "" || _csrf == "" || _statistics == "" || _sessdata == "" || _biliJct == "" || _uid == "" || _ckmd5 == "" || _sid == "" || _buvid == "" || _agent == "" || _eid == "") {
				Tools::errorPause("文件信息缺失");
			}
		} else {
			if (_itemId == "" || _accessKey == "" || _appkey == "" || _csrf == "" || _sessdata == "" || _biliJct == "" || _uid == "" || _ckmd5 == "" || _sid == "" || _agent == "") {
				Tools::errorPause("文件信息缺失");
			}
		}

		//setTimer();
		_timerMethod = 1;
		_isNewHost = true;
		_host = "api.live.bilibili.com";

		socketInit();
		sslInit();
		Tools::SetColorAndBackground(2, 0);
		cout << "\n>>初始化完成<<\n" << endl;
		Tools::SetColorAndBackground(15, 0);

		setMethod();

		string messageBody = urlEncode();
		string length = to_string(messageBody.length());

		if (_isAndroid) {
			if (!_isNewHost) {
				_stream << "POST https://api.bilibili.com/x/garb/v2/trade/create HTTP/1.1\r\n";
				_stream << "Host: api.bilibili.com\r\n";
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
				_stream << "x-bili-trace-id: " << generateTraceID(_saleTime) << "\r\n";
				_stream << "x-bili-aurora-eid: " << _eid << "\r\n";
				_stream << "x-bili-mid: " << _uid << "\r\n";
				_stream << "x-bili-aurora-zone: \r\n";
				_stream << "bili-http-engine: cronet\r\n";
				_stream << "Accept-Encoding: gzip\r\n\r\n";
				/*_stream << "Accept-Encoding: gzip, deflate, br\r\n\r\n";*/
				_stream << messageBody;
			} else {
				_stream << "POST https://api.live.bilibili.com/xlive/revenue/v2/order/createOrder HTTP/1.1\r\n";
				_stream << "Host: api.live.bilibili.com\r\n";
				_stream << "Connection: keep-alive\r\n";
				_stream << "Content-Length: " << length << "\r\n";
				_stream << "native_api_from: h5\r\n";
				_stream << "Cookie: SESSDATA=" << _sessdata << "; bili_jct=" << _biliJct << "; DedeUserID=" << _uid << "; DedeUserID__ckMd5=" << _ckmd5 << "; sid=" << _sid << "; Buvid=" << _buvid << "\r\n";
				_stream << "buvid: " << _buvid << "\r\n";
				_stream << "Accept: application/json, text/plain, */*\r\n";
				_stream << "Referer: https://www.bilibili.com/h5/mall/suit/detail?id=" << _itemId << "&navhide=1&f_source=shop&from=" << _shopFrom << "&from_id=\r\n";
				_stream << "Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n";
				_stream << "env: prod\r\n";
				_stream << "APP-KEY: android64\r\n";
				_stream << "User-Agent: " << _agent << "\r\n";
				_stream << "x-bili-trace-id: " << generateTraceID(_saleTime) << "\r\n";
				_stream << "x-bili-aurora-eid: " << _eid << "\r\n";
				_stream << "x-bili-mid: " << _uid << "\r\n";
				_stream << "x-bili-aurora-zone: \r\n";
				_stream << "bili-http-engine: cronet\r\n";
				//_stream << "Accept-Encoding: gzip, deflate, br\r\n\r\n";
				_stream << "Accept-Encoding: gzip\r\n\r\n";
				_stream << messageBody;
			}
		} else {
			_stream << "POST https://api.bilibili.com/x/garb/v2/trade/create HTTP/1.1\r\n";
			_stream << "Host: api.bilibili.com\r\n";
			_stream << "Accept: application/json, text/plain, */*\r\n";
			_stream << "Content-Type: application/x-www-form-urlencoded\r\n";
			_stream << "Accept-Language: zh-CN,zh-Hans;q=0.9\r\n";
			_stream << "Accept-Encoding: gzip\r\n";
			_stream << "Connection: keep-alive\r\n";
			_stream << "Cookie: SESSDATA=" << _sessdata << "; bili_jct=" << _biliJct << "; DedeUserID=" << _uid << "; DedeUserID__ckMd5=" << _ckmd5 << "; sid=" << _sid << "\r\n";
			_stream << "User-Agent: " << _agent << "\r\n";
			_stream << "Referer: https://www.bilibili.com/h5/mall/suit/detail?navhide=1" << "&from=" << _shopFrom << "&id=" << _itemId << "&f_source=shop" << "&native.theme=1\r\n";
			_stream << "Content-Length: " << length << "\r\n";
			_stream << "native_api_from: h5\r\n\r\n";
			_stream << messageBody;
		}

		memset(_sendData, '\0', sizeof(_sendData));
		memset(_sendHeader, '\0', sizeof(_sendHeader));
		memset(_sendBody, '\0', sizeof(_sendBody));

		string s = _stream.str();
		strcpy_s(_sendData, s.c_str());

		strcpy_s(_sendHeader, _sendData);
		_sendHeader[strlen(_sendHeader) - 1] = '\0';
		_sendBody[0] = _sendData[strlen(_sendData) - 1];
		_sendBody[1] = '\0';

		//cout << _sendData << endl;
		//system("pause");

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
		cout << "\n[1]新接口(默认, 安全); [2]老接口(快速, 危险)\n";
		Tools::SetColorAndBackground(9, 0);
		cout << "请输入选择数字: ";
		Tools::SetColorAndBackground(15, 0);
		_timerMethod = 1;
		char ch = getchar();
		if (ch == '2') {
			_isNewHost = false;
			_host = "api.bilibili.com";
		}
		else {
			_isNewHost = true;
			_host = "api.live.bilibili.com";
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
		string name = (*root)["data"]["name"].asString();
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		url = "https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf=" + _csrf + "&from=feed.card&item_id=" + _itemId + "&part=suit";
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, cookies, "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		long long begin_time = stoll((*root)["data"]["properties"]["sale_time_begin"].asString());
		_saleName = (*root)["data"]["name"].asString();
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		Tools::SetColorAndBackground(2, 0);
		cout << "\n当前设置抢购时间: " << Tools::stampTostandard(_saleTime) << "\n已检测到开售时间: " << Tools::stampTostandard(begin_time) << endl;
		Tools::SetColorAndBackground(14, 0);
		cout << "\n[1]修改为预售时间(默认); [2]10秒后购买10套EveOneCat2; [3]下个整点购买10套EveOneCat2; [4]保持设置\n";
		Tools::SetColorAndBackground(9, 0);
		cout << "请输入选择数字: ";
		Tools::SetColorAndBackground(15, 0);
		char ch = getchar();
		if (ch == '2') {
			_itemId = "32296";
			_buyNum = "10";
			_saleTime = time(0) + 10;
			_saleName = "EveOneCat2";
			Tools::SetColorAndBackground(14, 0);
			cout << "10秒后将发送10套EveOneCat2购买请求, 请确保账户余额小于590" << endl;
			Tools::SetColorAndBackground(15, 0);
			this_thread::sleep_for(chrono::milliseconds(2000));
		}
		else if (ch == '3') {
			_itemId = "32296";
			_buyNum = "10";
			_saleTime = (((long long)time(0) + 5) / 3600 + 1) * 3600;
			_saleName = "EveOneCat2";
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
			exit(0);
		}
		system("cls");
		Tools::SetColorAndBackground(11, 0);

		url = "https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf=" + _csrf + "&from=feed.card&item_id=" + _itemId + "&part=suit";
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, cookies, "", true, 4096);
		httpRequests->connectHost();
		root = httpRequests->getJson(true);
		_saleBP = stol((*root)["data"]["properties"]["sale_bp_forever_raw"].asString()) * 10 * stol(_buyNum);
		_saleName = (*root)["data"]["name"].asString();
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		url = "https://api.bilibili.com/x/garb/user/wallet";
		httpRequests = new HttpRequests(url, "https");
		httpRequests->generateMsg("GET", url, headers, cookies, "", false, 1024);
		httpRequests->connectHost();
		root = httpRequests->getJson(false);
		int bcoin = (int)((*root)["data"]["bcoin_balance"].asDouble() * 1000 + 0.5);
		delete httpRequests, root;
		httpRequests = nullptr;
		root = nullptr;

		cout << "抢购时间: " << Tools::stampTostandard(_saleTime) << endl;
		cout << "用户名: " << name << "  装扮名: " << _saleName << "  item_id: " << _itemId << endl;
		cout << "购买数量: " << _buyNum << "  总价(按原价算): " << _saleBP << "  B币余额(1000倍): " << bcoin << endl;
		if (_isSplitMsg) {
			cout << "isSplitMsg: " << "TRUE";
		}
		else
		{
			cout << "isSplitMsg: " << "FALSE";
		}
		if (_isAndroid) {
			cout << "  isAndroid: " << "TRUE";
		}
		else
		{
			cout << "  isAndroid: " << "FALSE";
		}
		if (_isNewHost) {
			cout << "  isNewHost: " << "TRUE";
		}
		else
		{
			cout << "  isNewHost: " << "FALSE";
		}
		cout << "  Predict_time: " << _predictTime << "ms" << endl;
		Tools::SetColorAndBackground(15, 0);
		return 0;
	}
	catch (...) {
		Tools::errorPause("setMothod error");
		return -1;
	}
}

char* BuySuit::getRecv() {
	return _rec;
}

BuySuit::~BuySuit()
{
	SSL_shutdown(_ssl);
	SSL_free(_ssl);
	SSL_CTX_free(_ctx);
	closesocket(_serverSocket);
	WSACleanup();
}

Json::Value BuySuit::getCookies() {
	try {
		Json::Value cookies;

		cookies["SESSDATA"] = _sessdata;
		cookies["bili_jct"] = _biliJct;
		cookies["DedeUserID"] = _uid;
		cookies["DedeUserID__ckMd5"] = _ckmd5;
		cookies["sid"] = _sid;
		cookies["Buvid"] = _buvid;

		return cookies;
	}
	catch (...) {
		Tools::errorPause("getCookies error");
	}
}

string BuySuit::getData() {
	try {
		stringstream body;
		body << "access_key=" << _accessKey;
		body << "&appkey=" << _appkey;
		body << "&csrf=" << _csrf;
		body << "&disable_rcmd=0";
		body << "&item_id=" << _itemId;
		body << "&part=suit";
		body << "&statistics=" << _statistics;
		body << "&ts=" << to_string(time(0));

		return getSign(body.str());
	}
	catch (...) {
		Tools::errorPause("getData error");
	}
}

string BuySuit::getSign(string form_data) {
	try {
		string app_sec;
		if (_isAndroid) {
			app_sec = "560c52ccd288fed045859ed18bffd973";
		}
		else {
			app_sec = "c2ed53a74eeefe3cf99fbd01d8c9c375";
		}
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
		//cout << encodedHexStr << endl;
		//system("pause");
		return form_data + "&sign=" + encodedHexStr;
	}
	catch (...) {
		Tools::errorPause("getSign error");
	}
}