# -*- coding:utf-8 -*-

from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import unquote
from threading import Thread
from typing import Union
import requests
import hashlib
import socket
import uuid
import time
import json
import ssl
import sys
import os

null = ""
true = True
false = False
flag = True
predict_time = 0 #ms 正提前, 负延后
listen_time = 5 #s
socket_time = 20 #s
timer = time.time() * 1000 - predict_time
buy_time_ary = "2022-09-28 19:00:00"
buy_time = int(time.mktime(time.strptime(buy_time_ary, "%Y-%m-%d %H:%M:%S")))
# buy_time = int(time.time()+70) #test&debug

class SuitSocket(object):
    def __init__(self, http_message_file, **kwargs):
        try:
            context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            context.verify_mode = ssl.CERT_REQUIRED
            ssl.Purpose.CLIENT_AUTH
            context.check_hostname = True
            context.load_default_certs()
            self.client = context.wrap_socket(socket.socket(), server_hostname="api.bilibili.com")
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

            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.50',
                'referer': 'https://www.bilibili.com/',
                'sec-ch-ua':'"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'sec-ch-ua-platform': '"Android"',
                'sec-ch-ua-mobile': '?1',
                'origin': 'https://www.bilibili.com',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'accept-encoding': 'gzip, deflate, br',
                'accept': 'application/json, text/plain, */*',
                'cookie': message_dict["api_cookie"]
            }

        except Exception as e:
            print(e)
            print("文件分析异常")
            os.system("pause")

        try:
            json_dict = json.loads(requests.get(url=f"https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf={__bili_jct}&from={__shop_from}&item_id={__item_id}&part=suit",headers=headers).text)
            sale_time = int(json_dict["data"]["properties"]["sale_time_begin"])
            item_name = json_dict["data"]["name"]
            print(f"建议提前校准时间!\n装扮item_id: {__item_id}\n装扮名: {item_name}\n抢购数量: {__buy_num}")
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(__sale_time)))
            true_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(sale_time)))
            # if sale_time != __sale_time:
            getchar = input(f"\n当前设置抢购时间: {now_time}\n检测到开售时间: {true_time}\n输入1保持设置, 输入2为12秒后测试, 输入3为下个整点测试, 否则修改为开售时间\n")
            if getchar != "1":
                if getchar == "2":
                    __sale_time = round(time.time()) + 12
                    __buy_num = 10
                    __item_id = 32296
                    print("测试装扮: EveOneCat2, 测试数量: 10, 请确保账户余额小于590")
                elif getchar == "3":
                    __sale_time = (int(time.time()-5)//3600+1)*3600
                    __buy_num = 10
                    __item_id = 32296
                    print("测试装扮: EveOneCat2, 测试数量: 10, 请确保账户余额小于590")
                else:
                    __sale_time = sale_time
                print("已修改抢购时间")
            true_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(__sale_time)))
            print(f"\n抢购时间: {true_time}")
            user_name = json.loads(requests.get(url = f'https://api.bilibili.com/x/space/acc/info?mid={message_dict["uid"]}', headers = headers).text)["data"]["name"]
            print(f"昵称: {user_name}")
            if time.time() >= __sale_time:
                print("\n抢购已过时...\n")
                os.system("pause")
                sys.exit(0)
            else:
                print(f"剩余抢购时间: {int(__sale_time - time.time())}s, 等待抢购...")

        except Exception as e:
            print(e)
            print("请求接口异常")
            os.system("pause")
        
        global timer
        timer = __sale_time * 1000 - predict_time

        try:
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
                # "from_id": "",
                "item_id": str(__item_id),
                "platform": "android",
                "statistics": __statistics,
                "ts": str(__sale_time)
            })
            body = self.AddFormDataSign(form_data_init)
            message = self.UpdateMessage(body, **message_dict)

            self.message_header = message[:-1]
            self.message_body = message[-1:]
            self.message = message

        except Exception as e:
            print(e)
            print("body编码异常")
            os.system("pause")

    def UpdateMessage(self, form_data: str, **kwargs):
        try:
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

            # message = f"POST /x/garb/v2/trade/create HTTP/1.1\r\n"
            # message += f"Host: {__host}\r\ncontent-length: {len(form_data)}\r\n"
            # message += f"native_api_from: h5\r\n"
            # # message += f"cookie: {__cookie_text}\r\n"
            # message += f"cookie: SESSDATA={__suit_cookie['SESSDATA']}\r\n"
            # message += f"cookie: bili_jct={__suit_cookie['bili_jct']}\r\n"
            # message += f"cookie: DedeUserID={__DedeUserID}\r\n"
            # message += f"cookie: DedeUserID__ckMd5={__suit_cookie['DedeUserID__ckMd5']}\r\n"
            # message += f"cookie: sid={__suit_cookie['sid']}\r\n"
            # message += f"cookie: Buvid={__suit_cookie['Buvid']}\r\n"
            # message += f"accept: application/json, text/plain, */*\r\n"
            # message += f"referer: {__referer}\r\n"
            # message += f"content-type: application/x-www-form-urlencoded; charset=utf-8\r\n"
            # message += f"env: prod\r\napp-key: android64\r\nuser-agent: {__UserAgent}\r\n"
            # message += f"x-bili-trace-id: {__TraceId}\r\nx-bili-aurora-eid: {__bili_eid}\r\n"
            # message += f"x-bili-mid: {__DedeUserID}\r\nx-bili-aurora-zone: \r\n"
            # message += f"bili-bridge-engine: cronet\r\naccept-encoding: gzip, deflate, br\r\n\r\n{form_data}"
            message = f"POST https://{__host}/x/garb/v2/trade/create HTTP/1.1\r\nHost: {__host}\r\n"
            message += f"Connection: Keep-Alive\r\nContent-Length: {len(form_data)}\r\nnative_api_from: h5\r\nCookie: {__cookie_text}\r\n"
            message += f"Accept: application/json, text/plain, */*\r\n"
            message += f"Referer: {__referer}\r\n"
            message += f"Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\nenv: prod\r\nAPP-KEY: android64\r\nUser-Agent: {__UserAgent}\r\n"
            message += f"x-bili-trace-id: {__TraceId}\r\nx-bili-aurora-eid: {__bili_eid}\r\n"
            message += f"x-bili-mid: {__DedeUserID}\r\nx-bili-aurora-zone: \r\n"
            message += f"bili-bridge-engine: cronet\r\nAccept-Encoding: gzip, deflate\r\n\r\n{form_data}"

            # print(message)
            # os.system("pause")
            return message.encode()
        except Exception as e:
            print(e)
            print("报文更新异常")
            os.system("pause")

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
        # print("\n",sign,"\n")
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
        value_dict["item_id"] = body_dict["item_id"]
        value_dict["statistics"] = unquote(params_dict["statistics"])
        value_dict["cookie"] = cookie_text
        value_dict["cookie-dict"] = cookie_dict
        value_dict["user-agent"] = body_dict["user-agent"]
        value_dict["aurora-eid"] = body_dict["x-bili-aurora-eid"]
        value_dict["api_cookie"] = body_dict["api"]
        value_dict["uid"] = body_dict["x-bili-mid"]

        return value_dict


class SuitBuy(SuitSocket):
    def __init__(self, http_message_file, **kwargs):
        super(SuitBuy, self).__init__(http_message_file, **kwargs)

    def __del__(self):
        self.client.close()

    def Link(self, port=443):
        global timer
        addr = ("127.0.0.1", 23333)
        addr = ("Moonkey233.top", 23333)
        self.timeSocket = socket.socket()
        self.timeSocket.connect(addr)
        print(f"{addr} 时间服务端连接成功")
        self.timeSocket.send(str(timer).encode('utf-8','ignore'))
        print(f"已发送购买时间: {timer}")

        while True:
            # session = requests.session()
            # session.get(url="https://app.bilibili.com/x/v2/splash/show")
            msg = int(self.timeSocket.recv(1024).decode("utf-8", "ingore"))
            if msg == 0:
                try:
                    s = time.time()
                    self.client.send(self.message)
                    response_ = self.client.recv(1)
                    e = time.time()

                    response = self.client.recv(4095)
                    self.client.close()
                    return (response_ + response).decode(errors='ignore'), (e - s) * 1000
                    # print(requests.get(url="https://app.bilibili.com/x/v2/splash/show").text)
                    # return "yes", 0

                except Exception as err:
                    print(err)
                    print("报文发送接收异常")
                    os.system("pause")
            elif msg == 2:
                # time.sleep()
                t = time.time()
                while True:
                    if time.time() - t >= 2:
                        break
                try:
                    self.client.connect((self.host, port))
                    print("Socket连接成功")
                except Exception as e:
                    print(e)
                    print("Socket连接异常")
                    os.system("pause")
            elif msg == -1:
                print(msg)
                break
            else:
                continue


        # try:
        #     self.client.connect((self.host, port))
        #     print("Socket连接成功")

        # except Exception as e:
        #     print(e)
        #     print("Socket连接异常")
        #     os.system("pause")

    def post(self):
        # try:
        #     session = requests.Session()
        #     while timer - int(json.loads(session.get(url="https://app.bilibili.com/x/v2/splash/show").text)["data"]["splash_request_id"][0:13]) > listen_time * 1000:
        #         time.sleep(1)
        #      session.close()

        # except Exception as e:
        #     print(e)
        #     print("时间请求异常")
        #     os.system("pause")

        # try:
        #     self.client.send(self.message_header)
        #     print("已发送不完整报文")

        # except Exception as e:
        #     print(e)
        #     print("报文发送异常")
        #     os.system("pause")

        # try:
        #     print("开始请求时间...")

        #     self.createThread()
        #     while True:
        #         if not flag:
        #             print("\nPRESSPRESSPRESSPRESSPRESSPRESSPRESSPRESSPRESSPRESS\n")
        #             break

        #     # global flag
        #     # session = requests.session()
        #     # while True:
        #     #     res = session.get(url="https://app.bilibili.com/x/v2/splash/show")
        #     #     server_time = int(json.loads(res.text)["data"]["splash_request_id"][0:13])
        #     #     if server_time >= timer:
        #     #         break

        # except Exception as e:
        #     print(e)
        #     print("时间请求异常")
        #     os.system("pause")

        # try:
        #     s = time.time()
        #     self.client.send(self.message_body)
        #     response_ = self.client.recv(1)
        #     e = time.time()

        #     response = self.client.recv(4095)
        #     self.client.close()
        #     return (response_ + response).decode(errors='ignore'), (e - s) * 1000

        # except Exception as e:
        #     print(e)
        #     print("报文发送接收异常")
        #     os.system("pause")
        pass

    def timerThread(self):
        global flag
        session = requests.Session()
        while flag:
            res = session.get(url="https://app.bilibili.com/x/v2/splash/show")
            server_time = int(json.loads(res.text)["data"]["splash_request_id"][0:13])
            if server_time >= timer:
                flag = False
                break

    def createThread(self):
        try:
            t1 = Thread(target=self.timerThread)
            t2 = Thread(target=self.timerThread)
            t3 = Thread(target=self.timerThread)
            t4 = Thread(target=self.timerThread)
            t5 = Thread(target=self.timerThread)
            t6 = Thread(target=self.timerThread)
            t7 = Thread(target=self.timerThread)
            t8 = Thread(target=self.timerThread)
            t9 = Thread(target=self.timerThread)
            t10 = Thread(target=self.timerThread)
            t11 = Thread(target=self.timerThread)
            t12 = Thread(target=self.timerThread)
            t13 = Thread(target=self.timerThread)
            t14 = Thread(target=self.timerThread)
            t15 = Thread(target=self.timerThread)
            t16 = Thread(target=self.timerThread)
            t17 = Thread(target=self.timerThread)
            t18 = Thread(target=self.timerThread)
            t19 = Thread(target=self.timerThread)
            t20 = Thread(target=self.timerThread)
            t21 = Thread(target=self.timerThread)
            t22 = Thread(target=self.timerThread)
            t23 = Thread(target=self.timerThread)
            t24 = Thread(target=self.timerThread)
            t25 = Thread(target=self.timerThread)
            t26 = Thread(target=self.timerThread)
            t27 = Thread(target=self.timerThread)
            t28 = Thread(target=self.timerThread)
            t29 = Thread(target=self.timerThread)
            t30 = Thread(target=self.timerThread)
            t31 = Thread(target=self.timerThread)
            t32 = Thread(target=self.timerThread)
            t33 = Thread(target=self.timerThread)
            t34 = Thread(target=self.timerThread)
            t35 = Thread(target=self.timerThread)
            t36 = Thread(target=self.timerThread)
            t37 = Thread(target=self.timerThread)
            t38 = Thread(target=self.timerThread)
            t39 = Thread(target=self.timerThread)
            t40 = Thread(target=self.timerThread)
            t41 = Thread(target=self.timerThread)
            t42 = Thread(target=self.timerThread)
            t43 = Thread(target=self.timerThread)
            t44 = Thread(target=self.timerThread)
            t45 = Thread(target=self.timerThread)
            t46 = Thread(target=self.timerThread)
            t47 = Thread(target=self.timerThread)
            t48 = Thread(target=self.timerThread)
            t49 = Thread(target=self.timerThread)
            t50 = Thread(target=self.timerThread)
            t51 = Thread(target=self.timerThread)
            t52 = Thread(target=self.timerThread)
            t53 = Thread(target=self.timerThread)
            t54 = Thread(target=self.timerThread)
            t55 = Thread(target=self.timerThread)
            t56 = Thread(target=self.timerThread)
            t57 = Thread(target=self.timerThread)
            t58 = Thread(target=self.timerThread)
            t59 = Thread(target=self.timerThread)
            t60 = Thread(target=self.timerThread)
            t61 = Thread(target=self.timerThread)
            t62 = Thread(target=self.timerThread)
            t63 = Thread(target=self.timerThread)
            t64 = Thread(target=self.timerThread)
            t65 = Thread(target=self.timerThread)
            t66 = Thread(target=self.timerThread)
            t67 = Thread(target=self.timerThread)
            t68 = Thread(target=self.timerThread)
            t69 = Thread(target=self.timerThread)
            t70 = Thread(target=self.timerThread)
            t71 = Thread(target=self.timerThread)
            t72 = Thread(target=self.timerThread)
            t73 = Thread(target=self.timerThread)
            t74 = Thread(target=self.timerThread)
            t75 = Thread(target=self.timerThread)
            t76 = Thread(target=self.timerThread)
            t77 = Thread(target=self.timerThread)
            t78 = Thread(target=self.timerThread)
            t79 = Thread(target=self.timerThread)
            t80 = Thread(target=self.timerThread)
            t81 = Thread(target=self.timerThread)
            t82 = Thread(target=self.timerThread)
            t83 = Thread(target=self.timerThread)
            t84 = Thread(target=self.timerThread)
            t85 = Thread(target=self.timerThread)
            t86 = Thread(target=self.timerThread)
            t87 = Thread(target=self.timerThread)
            t88 = Thread(target=self.timerThread)
            t89 = Thread(target=self.timerThread)
            t90 = Thread(target=self.timerThread)
            t91 = Thread(target=self.timerThread)
            t92 = Thread(target=self.timerThread)
            t93 = Thread(target=self.timerThread)
            t94 = Thread(target=self.timerThread)
            t95 = Thread(target=self.timerThread)
            t96 = Thread(target=self.timerThread)
            t97 = Thread(target=self.timerThread)
            t98 = Thread(target=self.timerThread)
            t99 = Thread(target=self.timerThread)
            t100 = Thread(target=self.timerThread)
            t101 = Thread(target=self.timerThread)
            t102 = Thread(target=self.timerThread)
            t103 = Thread(target=self.timerThread)
            t104 = Thread(target=self.timerThread)
            t105 = Thread(target=self.timerThread)
            t106 = Thread(target=self.timerThread)
            t107 = Thread(target=self.timerThread)
            t108 = Thread(target=self.timerThread)
            t109 = Thread(target=self.timerThread)
            t110 = Thread(target=self.timerThread)
            t111 = Thread(target=self.timerThread)
            t112 = Thread(target=self.timerThread)
            t113 = Thread(target=self.timerThread)
            t114 = Thread(target=self.timerThread)
            t115 = Thread(target=self.timerThread)
            t116 = Thread(target=self.timerThread)
            t117 = Thread(target=self.timerThread)
            t118 = Thread(target=self.timerThread)
            t119 = Thread(target=self.timerThread)
            t120 = Thread(target=self.timerThread)
            t121 = Thread(target=self.timerThread)
            t122 = Thread(target=self.timerThread)
            t123 = Thread(target=self.timerThread)
            t124 = Thread(target=self.timerThread)
            t125 = Thread(target=self.timerThread)
            t126 = Thread(target=self.timerThread)
            t127 = Thread(target=self.timerThread)
            t128 = Thread(target=self.timerThread)
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t6.start()
            t7.start()
            t8.start()
            t9.start()
            t10.start()
            t11.start()
            t12.start()
            t13.start()
            t14.start()
            t15.start()
            t16.start()
            t17.start()
            t18.start()
            t19.start()
            t20.start()
            t21.start()
            t22.start()
            t23.start()
            t24.start()
            t25.start()
            t26.start()
            t27.start()
            t28.start()
            t29.start()
            t30.start()
            t31.start()
            t32.start()
            t33.start()
            t34.start()
            t35.start()
            t36.start()
            t37.start()
            t38.start()
            t39.start()
            t40.start()
            t41.start()
            t42.start()
            t43.start()
            t44.start()
            t45.start()
            t46.start()
            t47.start()
            t48.start()
            t49.start()
            t50.start()
            t51.start()
            t52.start()
            t53.start()
            t54.start()
            t55.start()
            t56.start()
            t57.start()
            t58.start()
            t59.start()
            t60.start()
            t61.start()
            t62.start()
            t63.start()
            t64.start()
            # t65.start()
            # t66.start()
            # t67.start()
            # t68.start()
            # t69.start()
            # t70.start()
            # t71.start()
            # t72.start()
            # t73.start()
            # t74.start()
            # t75.start()
            # t76.start()
            # t77.start()
            # t78.start()
            # t79.start()
            # t80.start()
            # t81.start()
            # t82.start()
            # t83.start()
            # t84.start()
            # t85.start()
            # t86.start()
            # t87.start()
            # t88.start()
            # t89.start()
            # t90.start()
            # t91.start()
            # t92.start()
            # t93.start()
            # t94.start()
            # t95.start()
            # t96.start()
            # t97.start()
            # t98.start()
            # t99.start()
            # t100.start()
            # t101.start()
            # t102.start()
            # t103.start()
            # t104.start()
            # t105.start()
            # t106.start()
            # t107.start()
            # t108.start()
            # t109.start()
            # t110.start()
            # t111.start()
            # t112.start()
            # t113.start()
            # t114.start()
            # t115.start()
            # t116.start()
            # t117.start()
            # t118.start()
            # t119.start()
            # t120.start()
            # t121.start()
            # t122.start()
            # t123.start()
            # t124.start()
            # t125.start()
            # t126.start()
            # t127.start()
            # t128.start()
        except Exception as e:
            print(e)
            print("线程创建异常")
            os.system("pause")

def main():
    suit_buy = SuitBuy(
        http_message_file=r"./message.txt",

        # 可选
        add_month="-1",
        buy_num="1",
        coupon_token="",
        host="api.bilibili.com",
        f_source="shop",
        shop_from="feed.card",
        sale_time=buy_time
    )

    global timer
    timerSec = (timer + predict_time) / 1000
    while time.time() + socket_time + 10 < timerSec:
        sleep_time = int(timerSec - time.time() - socket_time)
        print(f"\n程序休眠{sleep_time}s\n")
        time.sleep(sleep_time)

    rep, t = suit_buy.Link()

    # rep, t = suit_buy.post()
    print(rep)
    print(t, "ms")
    print("抢购结束")
    os.system("pause")


if __name__ == '__main__':
    main()
