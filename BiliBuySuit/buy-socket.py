# -*- coding:utf-8 -*-

# https://github.com/lllk140

from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import unquote
from typing import Union
import hashlib
import socket
import uuid
import time
import ssl


class SuitSocket(object):
    def __init__(self, http_message_file, **kwargs):
        self.client = ssl.wrap_socket(socket.socket())
        with open(http_message_file, "rb") as message_file:
            message_content = message_file.read()
        message_file.close()
        __add_month = kwargs.get("add_month", "-1")
        __buy_num = kwargs.get("buy_num", "1")
        __coupon_token = kwargs.get("coupon_token", "")

        __host = kwargs.get("host", "api.bilibili.com")
        __f_source = kwargs.get("f_source", "shop")
        __shop_from = kwargs.get("shop_from", "feed.card")
        __sale_time_k = kwargs.get("sale_time", time.time())
        __sale_time = round(float(__sale_time_k))

        self.host = __host

        message_dict = self.ParseHttpMessage(message_content)
        message_dict.update({"shop_from": __shop_from})
        message_dict.update({"sale_time": __sale_time})
        message_dict.update({"f_source": __f_source})
        message_dict.update({"host": __host})

        __access_key = message_dict["access_key"]
        __app_key = message_dict["appkey"]
        __item_id = message_dict["item_id"]
        __bili_jct = message_dict["cookie-dict"]["bili_jct"]
        __statistics = message_dict["statistics"]

        form_data_init = urlencode({
            "access_key": __access_key,
            "add_month": str(__add_month),
            "appkey": str(__app_key),
            "buy_num": str(__buy_num),
            "coupon_token": str(__coupon_token),
            "csrf": str(__bili_jct),
            "currency": "bp",
            "disable_rcmd": "0",
            "f_source": str(__f_source),
            "from": str(__shop_from),
            "from_id": "",
            "item_id": str(__item_id),
            "platform": "android",
            "statistics": __statistics,
            "ts": str(__sale_time)
        })
        body = self.AddFormDataSign(form_data_init)
        message = self.UpdateMessage(body, **message_dict)

        self.message_header = message[:-1]
        self.message_body = message[-1:]

    def UpdateMessage(self, form_data: str, **kwargs):
        __f_source = kwargs.get("f_source")
        __shop_from = kwargs.get("shop_from")
        __sale_time = kwargs.get("sale_time")
        __host = kwargs.get("host")

        __suit_cookie: dict = kwargs.get("cookie-dict")
        __cookie_text = kwargs.get("cookie")
        __UserAgent = kwargs.get("user-agent")
        __item_id = kwargs.get("item_id")
        __bili_eid = kwargs.get("aurora-eid")
        __DedeUserID = __suit_cookie['DedeUserID']
        __TraceId = self.BiliTraceId(__sale_time)

        __referer = f"https://www.bilibili.com/h5/mall/suit/detail?id={__item_id}"
        __referer = __referer + f"&navhide=1&f_source={__f_source}&from={__shop_from}"

        message = f"POST https://{__host}/x/garb/v2/trade/create HTTP/1.1\r\n"
        message += f"native_api_from: h5\r\nCookie: {__cookie_text}\r\n"
        message += f"Accept: application/json, text/plain, */*\r\n"
        message += f"Referer: https://www.bilibili.com/h5/mall/suit/detail{__referer}\r\n"
        message += f"env: prod\r\nAPP-KEY: android\r\nUser-Agent: {__UserAgent}\r\n"
        message += f"x-bili-trace-id: {__TraceId}\r\nx-bili-aurora-eid: {__bili_eid}\r\n"
        message += f"x-bili-mid: {__DedeUserID}\r\nx-bili-aurora-zone: \r\n"
        message += f"Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n"
        message += f"Content-Length: {len(form_data)}\r\nHost: {__host}\r\n"
        message += f"Connection: Keep-Alive\r\nAccept-Encoding: gzip\r\n\r\n{form_data}"

        return message.encode()

    @staticmethod
    def BiliTraceId(_time: Union[int, float, str] = None):
        _time = float(_time) if _time else time.time()
        back6 = hex(round(_time / 256))
        front = str(uuid.uuid4()).replace("-", "")
        _data1 = front[6:] + back6[2:]
        _data2 = front[22:] + back6[2:]
        return f"{_data1}:{_data2}:0:0"

    @staticmethod
    def AddFormDataSign(form_data: str):
        app_sec = "560c52ccd288fed045859ed18bffd973"
        form_data_sec = f"{form_data}{app_sec}"
        md5_hashlib = hashlib.md5()
        md5_hashlib.update(form_data_sec.encode())
        sign = md5_hashlib.hexdigest()
        return form_data + f"&sign={sign}"

    @staticmethod
    def ParseHttpMessage(content: bytes):
        body_array, value_dict = content.split(b"\r\n"), dict()
        body_split = [tuple(i.split(b": ")) for i in body_array[1:]]
        body_dict = dict()
        for body_key in body_split:
            key_byte: bytes = body_key[0]
            key: str = key_byte.decode().lower()
            value = list(body_key)[1:]
            value_byte = b"".join(value)
            body_dict[key] = value_byte.decode()

        cookie_text: str = body_dict["cookie"]
        cookie_split = cookie_text.split("; ")
        cookie_list = [tuple(i.split("=")) for i in cookie_split]
        cookie_dict = {key: value for key, value in cookie_list}

        message_url: bytes = body_array[0].split(b" ")[1]
        url_params: str = urlsplit(message_url.decode("utf-8")).query
        params_split = [i.split("=") for i in url_params.split("&")]
        params_dict = {key: value for key, value in params_split}

        value_dict["access_key"] = params_dict["access_key"]
        value_dict["appkey"] = params_dict["appkey"]
        value_dict["item_id"] = params_dict["item_id"]
        value_dict["statistics"] = unquote(params_dict["statistics"])
        value_dict["cookie"] = cookie_text
        value_dict["cookie-dict"] = cookie_dict
        value_dict["user-agent"] = body_dict["user-agent"]
        value_dict["aurora-eid"] = body_dict["x-bili-aurora-eid"]

        return value_dict


class SuitBuy(SuitSocket):
    def __init__(self, http_message_file, **kwargs):
        super(SuitBuy, self).__init__(http_message_file, **kwargs)

    def __del__(self):
        self.client.close()

    def Link(self, port=443):
        self.client.connect((self.host, port))

    def test(self):
        self.client.send(self.message_header)

        s = time.time()
        self.client.send(self.message_body)
        response_ = self.client.recv(1)
        e = time.time()

        response = self.client.recv(4095)
        return (response_ + response).decode(), (e - s) * 1000


def main():
    suit_buy = SuitBuy(
        http_message_file=r"./test/message.txt",

        # 可选
        add_month="-1",
        buy_num="1",
        coupon_token="",
        host="api.bilibili.com",
        f_source="shop",
        shop_from="feed.card",
        sale_time=round(time.time())
    )

    # 跳出本地计时器后
    suit_buy.Link()

    # 等待服务器计时退出

    rep, t = suit_buy.test()
    print(rep)
    print(t, "ms")


if __name__ == '__main__':
    main()
