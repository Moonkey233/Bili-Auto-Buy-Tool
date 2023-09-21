#include "Timer.h"

int main() {
	bool isSplitMsg = false, isAndroid = true;
	int predict_timeMS = 0, local_time = 0, socket_time = 0;
	string host, buy_num, add_month, coupon_token, f_source, from, sale_time, message_path, timer_addr, timer_port;

	cout << "请输入抢购套数(整数, 取值范围[1, 10]): ";
	cin >> buy_num;
	getchar();

	cout << "请输入延迟(正数提前, 负数延后): ";
	cin >> predict_timeMS;
	getchar();

	BuySuit* buySuit = new BuySuit(
		host = "api.live.bilibili.com",
		buy_num = buy_num,
		add_month = "-1",
		coupon_token = "",
		f_source = "shop",
		from = "feed.card",
		sale_time = "2023:01:18 19:00:00",
		message_path = "message.txt",
		isSplitMsg = false,
		predict_timeMS,
		isAndroid = true
	);

	Timer* timer = new Timer(
		buySuit,
		local_time = 20,
		socket_time = 2,
		timer_port = "23333",
		timer_addr = "Moonkey233.top"
	);

	timer->waitLocalTime();
	timer->waitServerTime();
	this_thread::sleep_for(chrono::milliseconds(100));
	timer->reqOwnNumber();
	timer->writeLog();

	delete buySuit, timer;
	system("pause");
	return 0;
}
