#include "Timer.h"

int main() {
	bool isSplitMsg = false;
	int predict_timeMS = 0, local_time = 0, socket_time = 0;
	string buy_num, add_month, coupon_token, f_source, from, sale_time, message_path, timer_addr, timer_port;

	BuySuit *buySuit = new BuySuit(
		buy_num = "1",
		add_month = "-1",
		coupon_token = "",
		f_source = "shop",
		from = "feed.card",
		sale_time = "2022:10:07 19:00:00",
		message_path = "message.txt",
		isSplitMsg = true,
		predict_timeMS = 0
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

	delete buySuit, timer;
	system("pause");
	return 0;
}
