#include "BuySuit.h"
#include "ListenAPI.h"
#include "HttpRequests.h"
#include "Tools.h"

int main() {
	bool autoBuy = true;
	string buy_num, add_month, coupon_token, f_source, from, message_path;
	int sleepTimeMs = 200;

	BuySuit* buySuit = new BuySuit(
		buy_num = "1",
		add_month = "-1",
		coupon_token = "",
		f_source = "shop",
		from = "feed.card",
		message_path = "message.txt",
		autoBuy = false
	);

	ListenAPI* listenAPI = new ListenAPI(
		sleepTimeMs = 200,
		buySuit->_expSTART,
		buySuit->_expEND,
		buySuit->_itemId,
		buySuit->getCookies(),
		buySuit->getSpeedNum()
	);

	int true_number = listenAPI->startListen();
	buySuit->autoSetBuyNum(true_number);
	buySuit->generateMessage();
	//system("pause");
	buySuit->connectServer();
	buySuit->post();

	delete buySuit, listenAPI;
	system("pause");
	return 0;
}
