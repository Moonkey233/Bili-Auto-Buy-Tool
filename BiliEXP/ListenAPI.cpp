#include "ListenAPI.h"
#include <thread>

ListenAPI::ListenAPI(int sleepTimeMS, int start, int end, string id, Json::Value cookies, int speedNum)
{
	_sleepTimeMS = sleepTimeMS;
	_start = start;
	_end = end;
	_cookies = cookies;
	_itemId = id;
	_speedNum = speedNum;
	//cout << "监听间隔: " << _sleepTimeMS << " ms" << endl;
}

ListenAPI::~ListenAPI()
{

}

int ListenAPI::startListen() {
	try {
		string url = "https://api.bilibili.com/x/garb/rank/fan/recent?item_id=" + _itemId;
		string json_str = "{\"user-agent\": \"Mozilla/5.0 (Linux; Android 12; M2011K2C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 os/android model/M2011K2C build/7040300 osVer/12 sdkInt/31 network/1 BiliApp/7040300 mobi_app/android channel/xiaomi Buvid/XYB74C8BADCB34811772C27D61F4184947D55 sessionID/51afacc7 innerVer/7040310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0\",\"referer\": \"https://www.bilibili.com/\",\"sec-fetch-site\": \"same-site\",\"sec-fetch-mode\": \"cors\",\"sec-fetch-dest\": \"empty\",\"sec-ch-ua-platform\": \"Android\",\"sec-ch-ua-mobile\": \"?1\",\"origin\": \"https://www.bilibili.com\",\"accept-language\": \"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\",\"accept\": \"application/json, text/plain, */*\",\"connection\":\"keep-alive\"}";
		Json::Reader reader;
		Json::Value headers;
		Json::Value* root;
		reader.parse(json_str, headers);

		int true_number = 0, now_number = 0;
		bool flag = true, isReq = false;
		HttpRequests* req = nullptr;
		int cnt = 0;
		clock_t sleepTime = 0;

		while (flag)
		{
			req = new HttpRequests("api.bilibili.com", "https");
			req->generateMsg("GET", url, headers, _cookies, "", true, 4096);
			req->connectHost();

			for (int i = 0; i < 100 && flag; i++) {
				isReq = false;
				while (flag) {
					if (clock() - sleepTime > _sleepTimeMS) {
						sleepTime = clock();
						cnt++;
						//this_thread::sleep_for(chrono::milliseconds(_sleepTimeMS));
						//cout << req->request() << endl;
						root = req->getJson(true);
						int j = 0;
						now_number = (*root)["data"]["rank"][j]["number"].asInt();
						true_number = now_number > true_number ? now_number : true_number;
						cout << "\rCount: " << cnt << " SleepTime: " << _sleepTimeMS << " ms" << " 当前播报: " << true_number;
						isReq = true;
						delete root;
						root = nullptr;
					} //if

					if (true_number >= _start && true_number <= _end) {
						flag = false; //for break
						break; //while
					}
					else if (true_number < _start) {
						if (true_number >= _start - _speedNum && _sleepTimeMS > 150) {
							cout << "\n加速频率..." << endl;
							_sleepTimeMS = 150;
						}
						if (i >= 99 && isReq) {
							break; //while
						}
					}
					else {
						Tools::errorPause("\n预期区间已过, 监听抢购结束");
						exit(0);
					}
					if (isReq) {
						break; //while
					}
				} //while
			} //for
			req->closeConnect();
			delete req;
			req = nullptr;
		}
		return true_number;
	}
	catch (...) {
		Tools::errorPause("\nreq error");
	}
}