# Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright © 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

import time
import uuid
import json
import queue
import hashlib
import requests
from threading import Thread
from urllib.parse import urlencode

#变化值
num_end = 25 #1 ~ 30
max_win = 2 #指尾号前最多多少号也可以拿, 如20000总量, max_win = 2则期望获得19999 ~ 20000
max_time = 175 #一个订单最多持续的时间
total = 30000 #库存总数
item_id = 37825 #购买装扮id
sleepTime = 0.2 #购买请求失败后停止多久重试 防频繁
uid = "1709355263" #购买者uid
version = "6.88.0" #抓包版本号
eid = "UFMBT1IBA1MBXw==" #有时效的用户登录验证, 抓包
csrf = "c01f559ce605af895426d9ee6a2a936a" #有时效的用户登录验证, 抓包
access_key = "6c32619d41276e336c6b7aa8ab949d91" #有时效的用户登录验证, 抓包
cookies = { #有时效的用户登录验证, 抓包
    "SESSDATA":"7c7d21e1%2C1678067796%2Caab69891",
    "DedeUserID__ckMd5":"22a2d87c4842710c",
    "sid":"gbap0ofd",
    "Buvid":"XX185A1175A6B2CC78AC6AC2FDB57813F6EE1",
    "bili_jct":csrf,
    "DedeUserID":uid
}
#有时效的用户登录验证, 抓包
agent = "Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 os/android model/Mi 10 build/6880300 osVer/11 sdkInt/30 network/2 BiliApp/6880300 mobi_app/android channel/xiaomi Buvid/XX185A1175A6B2CC78AC6AC2FDB57813F6EE1 sessionID/bca305d3 innerVer/6880310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.88.0 os/android model/Mi 10 mobi_app/android build/6880300 channel/xiaomi innerVer/6880310 osVer/11 network/2"
api_header = {
    'user-agent':'Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 os/android model/Mi 10 build/6880300 osVer/11 sdkInt/30 network/2 BiliApp/6880300 mobi_app/android channel/xiaomi Buvid/XX185A1175A6B2CC78AC6AC2FDB57813F6EE1 sessionID/bca305d3 innerVer/6880310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.88.0 os/android model/Mi 10 mobi_app/android build/6880300 channel/xiaomi innerVer/6880310 osVer/11 network/2',
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': r'''buvid3=DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc; i-wanna-go-back=-1; _uuid=B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc; buvid4=5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==; buvid_fp_plain=undefined; buvid_fp=12ec06c99d3813205d1bd6fc4978b706; rpdid=|(J~JY|YuRY~0J'uYR~k~lkYY; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5516474282866283; nostalgia_conf=-1; blackside_state=0; hit-dyn-v2=1; CURRENT_QUALITY=120; bp_video_offset_416166928=697567164921544800; bp_video_offset_215177187=697895274748575900; fingerprint3=3f1b7a30861b19380f9fd5561f012e65; bp_video_offset_392774666=698945677744406500; PVID=2; is-2022-channel=1; fingerprint=5f9964bfeda77c7caa29037eff00c242; b_nut=100; b_lsid=5DE8E5810_1831FFB1C05; innersign=0; b_ut=7; SESSDATA=c6945334,1678245764,fbde8*91; bili_jct=a664a3a76d1ae9355d075cfe1f917aa3; DedeUserID=1709355263; DedeUserID__ckMd5=22a2d87c4842710c; CURRENT_FNVAL=16; sid=54tia1hl; bp_video_offset_1709355263=703748855648223200'''
}

#不变值
null = ""
timer = 0
fresh_sec = 0.1
true_number = 0
list_num = 0
order_num = 0
item_num = 0
oldest_order = ()
# order_list = queue.Queue()
order_list = []

app_key = "1d8b6e7d45233436"
app_sec = "560c52ccd288fed045859ed18bffd973"
url = "https://api.bilibili.com/x/garb/v2/trade/create"
cancel_url = "https://api.bilibili.com/x/garb/v2/trade/cancel"
num_url = f'https://api.bilibili.com/x/garb/order/item/count/unpaid?item_id={item_id}'
now_url = f'https://api.bilibili.com/x/garb/rank/fan/recent?item_id={item_id}'
refer = f"https://www.bilibili.com/h5/mall/suit/detail?navhide=1&from=icon.category&id={item_id}&f_source=shop&native.theme=1"
cancel_refer = "https://www.bilibili.com/h5/mall/v2/order?navhide=1"
headers = {
    "Host": "api.bilibili.com",
    "content-length": "",
    "native_api_from": "h5",
    "accept": "application/json, text/plain, */*",
    "referer": "",
    "content-type": "application/x-www-form-urlencoded; charset=utf-8",
    "env": "prod",
    "app-key": "android64",
    "user-agent": agent,
    "x-bili-trace-id": "",
    "x-bili-aurora-eid": eid,
    "x-bili-mid": uid,
    "x-bili-aurora-zone": "",
    "bili-bridge-engine": "cronet",
    "accept-encoding": "gzip, deflate, br"
}

def GenerateTraceID():
    """计算trace_id并返回"""
    trace_id_uid = str(uuid.uuid4()).replace("-", "")[0:26].lower()
    trace_id_hex = hex(int(round(time.time()) / 256)).lower().replace("0x", "")
    trace_id = trace_id_uid + trace_id_hex + ":" + trace_id_uid[-10:] + trace_id_hex + ":0:0"
    return trace_id

def SessionDataAddMd5Sign(data_str):
    """ 计算sign并且在表单添加sign """
    md5_data = f"{data_str}{app_sec}"
    md5_ = hashlib.md5()
    md5_.update(md5_data.encode())
    sign = md5_.hexdigest()
    all_data = data_str + f"&sign={sign}"
    return all_data, str(len(all_data))

def GenerateCancelOrderContent(order_id):
    """ 生成取消定单用表单 """
    statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
    statistics = statistics_.replace("__version__", version)
    data_str = urlencode({
        "access_key": access_key, "appkey": app_key,
        "csrf": csrf, "disable_rcmd": "0",
        "order_id": str(order_id), "statistics": statistics,
        "ts": str(round(time.time()))
    })
    return SessionDataAddMd5Sign(data_str)

def GenerateSuitBuyContent(buy_num, add_month):
    """ 生成下单用表单 """
    statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
    statistics = statistics_.replace("__version__", version)
    data_str = urlencode({
        "access_key": access_key, "add_month": add_month,
        "appkey": app_key, "buy_num": str(buy_num),
        "coupon_token": "", "csrf": csrf,
        "currency": "bp", "disable_rcmd": "0",
        "f_source": "shop", "from": "icon.category", "from_id": "",
        "item_id": str(item_id),
        "platform": "android", "statistics": statistics,
        "ts": str(round(time.time()))
    })
    return SessionDataAddMd5Sign(data_str)

def suitBuyPost(n):
    global order_num
    while n > 0:
        data, length = GenerateSuitBuyContent(n, -1)
        headers["content-length"] = length
        headers["referer"] = refer
        headers["x-bili-trace-id"] = GenerateTraceID()
        res = requests.post(url = url, cookies = cookies, headers = headers, data = data)
        json_data = json.loads(res.text)
        if json_data["code"] == 0:
            break
        else:
            n -= 1
            time.sleep(sleepTime)
    print(res.text, n)
    order_list.append((json_data["data"]["order_id"], time.time(), n))
    order_num += n

def suitCancelPost(id):
    global order_num
    for i in order_list:
        if i[0] == id:
            oldest_order = i
            cancel_data, cancel_length = GenerateCancelOrderContent(oldest_order[0])
            headers["content-length"] = cancel_length
            headers["referer"] = cancel_refer
            headers["x-bili-trace-id"] = GenerateTraceID()
            cancel_res = requests.post(url = cancel_url, cookies = cookies, headers = headers, data = cancel_data)
            print(cancel_res.text)
            order_num -= oldest_order[2]
            break

def case4case0(t):
    #申请订单
    if list_num == 0:
        buy_num = int(t / 3)
    elif list_num == 1:
        buy_num = int((t - order_num) / 2)
    else:
        buy_num = t - order_num
    if item_num >= buy_num:
        suitBuyPost(buy_num)
    else:
        suitBuyPost(item_num) #成功case 6 失败case 2

def inputend():
    global num_end
    while True:
        try:
            n = int(input())
            num_end = n if n >= max_win else max_win
            print(f"num_end现在为: {num_end}")
        except:
            num_end = max_win
            print(f"num_end现在为: {num_end}")

# def timer():
#     for i in order_list:
#         if time.time() - i[1] > max_time:
#             suitCancelPost()
#             suitBuyPost()

t1 = Thread(target = inputend)
t1.start()

while True:
    if time.time() - timer > fresh_sec:
        timer = time.time()
        temp = num_end

        flag = 0
        # order_num = 0
        isWin = False

        #查即将超时订单
        for i in order_list:
            if time.time() - i[1] > max_time:
                suitCancelPost(i[0])
                time.sleep(0.5)

        #查订单数
        list_num = len(order_list)

        #查套数
        # for i in order_list:
        #     order_num += i[2]

        #查库存
        reponse = requests.get(url = num_url, headers = api_header)
        # print(reponse.text)
        item_num = json.loads(reponse.text)["data"]["surplus"]
        # item_num = 500

        #查播报
        # reponse = requests.get(url = now_url, headers = api_header)
        # now_num = json.loads(reponse.text)["data"]["rank"][0]["number"]
        # true_number = now_num if now_num > true_number else true_number
        true_number = 29950

        #分析情况
        if true_number >= total  - max_win and order_num > 0 and order_num <= max_win: #win
            isWin = True

        if true_number >= total - max_win:
            flag += 4
        if item_num == 0:
            flag += 2
        if order_num == temp:
            flag += 1

        if flag == 0: #买就对了 进case1 case2 case3
            case4case0(temp)
        elif flag == 1: #正常等待 进case3
            pass
        elif flag == 2: #等待case0
            pass
        elif flag == 3: #正常等待 进case7
            if order_num + true_number == total:
                print("全部订单已经被你占有") #通知全占有
        elif flag == 4: #成功购买则进入case6/case7
            case4case0(temp)
        elif flag == 5: #不存在的情况
            pass
        elif flag == 6: #order_num > 0则win 否则尝试等待case4抢购
            if order_num > 0:
                isWin = True
            else:
                pass
        elif flag == 7: #case7 胜利 正常计时, 通知
            isWin = True

        if isWin:
            print("您已经获胜, 请及时支付订单...")