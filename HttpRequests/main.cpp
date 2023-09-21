#include "HttpRequests.h"

int main() {
	std::string json_str = "{\"user-agent\": \"ÖÐÎÄMozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.50\",\"referer\": \"https://www.bilibili.com/\",\"sec-fetch-site\": \"same-site\",\"sec-fetch-mode\": \"cors\",\"sec-fetch-dest\": \"empty\",\"sec-ch-ua-platform\": \"Android\",\"sec-ch-ua-mobile\": \"?1\",\"origin\": \"https://www.bilibili.com\",\"accept-language\": \"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\",\"accept\": \"application/json, text/plain, */*\",\"connection\":\"keep-alive\"}";
	Json::Reader reader;
	Json::Value headers;
	//Json::Value cookies;
	Json::Value root;
	reader.parse(json_str, headers);
	std::string url = "https://api.bilibili.com/x/space/acc/info?mid=123456";
	//url = "https://app.bilibili.com/x/v2/splash/show";
	//url = "https://api.bilibili.com/x/garb/v2/mall/suit/detail?from=feed.card&item_id=32296&part=suit";
	url = "127.0.0.1";
	json_str = "{\"buvid3=\":\"DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc\",\"i-wanna-go-back\":\"-1\",\"_uuid\":\"B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc\",\"buvid4\":\"5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==\",\"buvid_fp_plain\":\"undefined\",\"buvid_fp\":\"12ec06c99d3813205d1bd6fc4978b706\",\"rpdid\":\"|(J~JY|YuRY~0J'uYR~k~lkYY\",\"CURRENT_BLACKGAP\":\"0\",\"LIVE_BUVID\":\"AUTO5516474282866283\",\"nostalgia_conf\":\"-1\",\"blackside_state\":\"0\",\"hit-dyn-v2\":\"1\",\"is-2022-channel\":\"1\",\"b_nut\":\"100\",\"b_ut\":\"5\",\"bp_video_offset_1709355263\":\"708216085546008700\",\"bp_article_offset_1709355263\":\"708203625829105700\",\"DedeUserID\":\"215177187\",\"DedeUserID__ckMd5\":\"db23a7f040ba3d37\",\"CURRENT_FNVAL\":\"4048\",\"SESSDATA\":\"9afd8866\",\"bili_jct=\":\"1680109656\",\"fingerprint\":\"2fcb4*a1\",\"CURRENT_QUALITY\":\"0\",\"PVID\":\"1\",\"sid\":\"6xyragrl\",\"fingerprint3\":\"eeda4c17fd99720ae6dec25b56a727a8\"}";
	//reader.parse(json_str, cookies);
	std::string cookies = "buvid3=DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc; i-wanna-go-back=-1; _uuid=B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc; buvid4=5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==; buvid_fp_plain=undefined; buvid_fp=12ec06c99d3813205d1bd6fc4978b706; rpdid=|(J~JY|YuRY~0J'uYR~k~lkYY; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5516474282866283; nostalgia_conf=-1; blackside_state=0; hit-dyn-v2=1; is-2022-channel=1; b_nut=100; b_ut=5; bp_video_offset_1709355263=708216085546008700; bp_article_offset_1709355263=708203625829105700; DedeUserID=215177187; DedeUserID__ckMd5=db23a7f040ba3d37; fingerprint=e03ad5dea8dafbc2a18b083ec6c69573; fingerprint3=eeda4c17fd99720ae6dec25b56a727a8; PVID=1; SESSDATA=bf6f65d4,1680402964,6b3a2*a1; bili_jct=c9cf5f3fa719c074a636c0ffd6836467; sid=7d7qvb2l; CURRENT_FNVAL=4048; CURRENT_QUALITY=116";
	HttpRequests *req = new HttpRequests(url, "23333");
	//req->generateMsg("GET", url, headers, cookies, "", false, 4096);
	req->generateMsg("GET", url, Json::nullValue, Json::nullValue, "", false, 1024);
	
	if (req->connectHost() != 0) {
		std::cout << "connection failed!" << std::endl;
	}
	std::cout << req->request(true) << std::endl;
	system("pause");
	delete req;
	return 0;
}