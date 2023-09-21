# -*- coding:utf-8 -*-

# https://github.com/lllk140

from requests.utils import cookiejar_from_dict
from urllib.parse import urlencode
import datetime
import requests
import hashlib
import time
import uuid
import sys


class SuitNumberBuyValue(object):
    app_sec = "560c52ccd288fed045859ed18bffd973"  # ����sign�õ�

    def __init__(self, **kwargs):
        """
        app_key: AppKey, Default 1d8b6e7d45233436
        system_version: ϵͳ��׿�汾, Default 9
        channel: ��������, Default html5_download
        buv_id: �豸��ʶ, Default XY + "0" * 35
        access_key: �û���ʶ, Default None
        version: APP�汾�ַ���, Default 6.83.0
        phone: �ֻ��ͺ�, Default M2007J22C
        build: APP�汾����, Default 68300100
        sdk_int: ��׿sdk�汾, Default 28
        item_id: װ���ʶ, Default None
        cookie: �û���ʶ, Default None
        """
        self.app_key: str = kwargs.get("app_key", "1d8b6e7d45233436")
        self.system_version: str = kwargs.get("system_version", "9")
        self.channel: str = kwargs.get("channel", "html5_download")
        self.buv_id: str = kwargs.get("buv_id", f"XY{'0' * 35}")
        self.access_key: str = kwargs.get("access_key", None)
        self.version: str = kwargs.get("version", "6.83.0")
        self.phone: str = kwargs.get("phone", "M2007J22C")
        self.build: str = kwargs.get("build", "68300100")
        self.sdk_int: str = kwargs.get("sdk_int", "28")
        self.item_id: str = kwargs.get("item_id", None)
        self.cookie: dict = kwargs.get("cookie", None)

        """
        ����, �ж�[access_key, item_id, cookie ...]��Щ��Ҫֵ
        """
        assert self.access_key, "access_key is a necessary key/value"
        assert self.item_id, "item_id is a necessary key/value"
        assert self.cookie, "cookie is a necessary key/value"

    @staticmethod
    def PrintLog(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        """ ��ʱ���ӡ """
        time_str = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}]"
        time_str_c = "\033[31;1m" + time_str + "\033[0m"
        print(time_str_c, *objects, sep=sep, end=end, file=file, flush=flush)


class SuitNumberBuy(SuitNumberBuyValue):
    def __init__(self, **kwargs):
        """ ��ʼ��, ����Session """
        super(SuitNumberBuy, self).__init__(**kwargs)
        __referer = f"https://www.bilibili.com/h5/mall/suit/detail?id={self.item_id}&navhide=1"
        self.SuitSession = requests.Session()
        self.SuitSession.trust_env = False
        self.SuitSession.proxies = {"http": None, "https": None}
        self.SuitSession.cookies = cookiejar_from_dict(self.cookie)
        self.SuitSession.headers.update({"Accept": "application/json, text/plain, */*"})
        self.SuitSession.headers.update({"Accept-Encoding": "gzip"})
        self.SuitSession.headers.update({"User-Agent": self.__GenerateUserAgent()})
        self.SuitSession.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"})
        self.SuitSession.headers.update({"APP-KEY": "android"})
        self.SuitSession.headers.update({"env": "prod"})
        self.SuitSession.headers.update({"native_api_from": "h5"})
        self.SuitSession.headers.update({"Referer": __referer})
        self.SuitSession.headers.update({"x-bili-aurora-eid": ""})
        self.SuitSession.headers.update({"x-bili-aurora-zone": ""})
        self.SuitSession.headers.update({"x-bili-mid": f"{self.cookie['DedeUserID']}"})
        self.SuitSession.headers.update({"x-bili-trace-id": self.__GenerateTraceId()})
        self.SuitSession.headers.update({"Connection": "keep-alive"})
        self.SuitSession.headers.update({"Host": "api.biliapi.net"})

    def __GenerateUserAgent(self):
        """ ��, ����ǿ��֢д��������, ��\\Ҳ���� """
        user_agent_list = [
            f"Mozilla/5.0 (Linux; Android {self.system_version}; {self.phone} Build/OPR1.170623.027; wv)",
            f"AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36",
            f"os/android model/{self.phone} build/{self.build} osVer/{self.system_version} sdkInt/{self.sdk_int}",
            f"network/2 BiliApp/{self.build} mobi_app/android channel/{self.channel} Buvid/{self.buv_id}",
            f"innerVer/{self.build} c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 {self.version} os/android",
            f"model/{self.phone} mobi_app/android build/{self.build} channel/{self.channel} innerVer/{self.build}",
            f"osVer/{self.system_version} network/2"
        ]
        return " ".join(user_agent_list)

    def __GenerateTraceId(self):
        """ ����, ���˿�, ��uuid4�Ǹ��������ֻ�ץ���� """
        a, b = "".join(str(uuid.uuid4()).split("-")), hex(int(self.item_id))
        return a[0:26] + b[2:8] + ":" + a[16:26] + b[2:8] + ":0:0"

    def __GenerateSuitBuyContent(self, buy_num, add_month):
        """ �����µ��ñ� """
        statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
        statistics = statistics_.replace("__version__", self.version)
        data_str = urlencode({
            "access_key": self.access_key, "add_month": add_month,
            "appkey": self.app_key, "buy_num": str(buy_num),
            "coupon_token": "", "csrf": self.cookie["bili_jct"],
            "currency": "bp", "disable_rcmd": "0",
            "f_source": "shop", "from": "feed.card", "from_id": "",
            "item_id": str(self.item_id),
            "platform": "android", "statistics": statistics,
            "ts": str(round(time.time()))
        })
        return self.__SessionDataAddMd5Sign(data_str)

    def __GenerateCancelOrderContent(self, order_id):
        """ ����ȡ�������ñ� """
        statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
        statistics = statistics_.replace("__version__", self.version)
        data_str = urlencode({
            "access_key": self.access_key, "appkey": self.app_key,
            "csrf": self.cookie["bili_jct"], "disable_rcmd": "0",
            "order_id": str(order_id), "statistics": statistics,
            "ts": str(round(time.time()))
        })
        return self.__SessionDataAddMd5Sign(data_str)

    def __SessionDataAddMd5Sign(self, data_str):
        """ ����sign�����ڱ����sign """
        md5_data = f"{data_str}{self.app_sec}"
        md5_ = hashlib.md5()
        md5_.update(md5_data.encode())
        sign = md5_.hexdigest()
        all_data = data_str + f"&sign={sign}"
        return all_data, str(len(all_data))

    def GetNewSuitNumber(self, number=0):
        """ ��ȡȷ�ϸ��������±�� """
        url = f"https://api.bilibili.com/x/garb/rank/fan/recent"
        response = self.SuitSession.get(url, params={"item_id": self.item_id})
        return response.json()["data"]["rank"][number]["number"]

    def GetSuitCount(self):
        """ �鿴��� """
        url = f"https://api.biliapi.net/x/garb/order/item/count/unpaid"
        response = self.SuitSession.get(url, params={"item_id": self.item_id})
        return response.json()["data"]["surplus"]

    def GetOrderList(self):
        """ �鿴����״̬ """
        url = "https://api.bilibili.com/x/garb/order/list"
        response = self.SuitSession.get(url, params={"state": "1"})
        list_order = response.json()["data"]["list"]
        return list() if list_order is None else list_order

    def PlaceOrder(self, buy_num, add_month: str = "-1"):
        """ �µ�װ�� """
        url = "https://api.bilibili.com/x/garb/v2/trade/create"
        content, content_len = self.__GenerateSuitBuyContent(buy_num, add_month)
        headers = self.SuitSession.headers.copy()
        headers.update({"Content-Length": content_len})
        response = self.SuitSession.post(url, data=content, headers=headers)
        return response

    def CancelOrder(self, order_id):
        """ ȡ������ """
        url = "https://api.biliapi.net/x/garb/v2/trade/cancel"
        content, content_len = self.__GenerateCancelOrderContent(order_id)
        headers = self.SuitSession.headers.copy()
        headers.update({"Content-Length": content_len})
        response = self.SuitSession.post(url, data=content, headers=headers)
        return response

    def run(self, max_number, time_sleep=0.2):
        """
        ��ֻ�ǰѸ��õĶ�����д�ø���, �߼��Լ�д(
        û��"__"��ͷ��function���ǿɵ��õ�
        """
        ...


if __name__ == '__main__':
    Client = SuitNumberBuy(
        cookie={
            "SESSDATA": "",
            "bili_jct": "",
            "DedeUserID": "",
            "DedeUserID__ckMd5": "",
            "sid": "",
            "Buvid": ""
        },
        buv_id="",
        access_key="",
        app_key="1d8b6e7d45233436",
        item_id="37388",
        phone="M2007J22C",
        channel="yingyongbao",
        system_version="9",
        sdk_int="28",
        version="6.83.0",
        build="68300100"
    )
    Client.run(10)

    # print(Client.GetOrderList())
    # print(Client.CancelOrder("xxxxxx"))