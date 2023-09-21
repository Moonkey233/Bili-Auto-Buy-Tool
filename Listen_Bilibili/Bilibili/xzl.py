# coding:UTF-8
# Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright ? 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

import os
import sys
import time
import json
import uuid
import socket
import ctypes
import datetime
import hashlib
import requests
from urllib.parse import urlencode

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

#变化值
local_timer = True
predict_time = 1 #负数提前, 正数延后, 单位: 秒
buy_num = 1 #购买套数m 建议大前期号为1, 至多2
item_id = 39105 #购买装扮id
# item_id = 32296 #test
uid = "86501805" #购买者uid
buy_time_ary = "2022-10-27 20:00:00" #装扮开售标准时间
buy_time = int(time.mktime(time.strptime(buy_time_ary, "%Y-%m-%d %H:%M:%S")))
# buy_time = int(time.time() + 15)
version = "7.0.0" #抓包版本号
eid = "WVIERlAMBlQ=" #有时效的用户登录验证, 抓包
csrf = "4417ff1cf8d47061639800214b5ee5b9" #有时效的用户登录验证, 抓包
access_key = "4a729ec6525daccda4a083d1ec3080a1" #有时效的用户登录验证, 抓包
cookies = { #有时效的用户登录验证, 抓包
    "SESSDATA":"ef449e40%2C1681810927%2C3835cfa1",
    "DedeUserID__ckMd5":"1ee0f49081851542",
    "sid":"6s4444bl",
    "Buvid":"XY0950501D960988398A7554196528B1DE9E4",
    "bili_jct":csrf,
    "DedeUserID":uid
}
#有时效的用户登录验证, 抓包
agent = "Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 os/android model/MI 8 SE build/7000400 osVer/10 sdkInt/29 network/2 BiliApp/7000400 mobi_app/android channel/xiaomi Buvid/XY0950501D960988398A7554196528B1DE9E4 sessionID/54141452 innerVer/7000410 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 7.0.0 os/android model/MI 8 SE mobi_app/android build/7000400 channel/xiaomi innerVer/7000410 osVer/10 network/2"
api_cookie = "SESSDATA="+cookies["SESSDATA"]+"; DedeUserID__ckMd5="+cookies["DedeUserID__ckMd5"]+"; sid="+cookies["sid"]+"; Buvid="+cookies["Buvid"]+"; bili_jct="+cookies["bili_jct"]+"; DedeUserID="+cookies["DedeUserID"]

header = {
    'user-agent': agent,
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': api_cookie
} #cookie也要抓

time_headers = { #app开屏抓包获取时间戳
    "Host": "app.bilibili.com",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.50',
    "accept-encoding": "gzip"
}

#不变值
app_key = "1d8b6e7d45233436"
app_sec = "560c52ccd288fed045859ed18bffd973"
url = "https://api.bilibili.com/x/garb/v2/trade/create"
time_url = "https://app.bilibili.com/x/v2/splash/show"
name_url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}'
lock_url = "https://api.bilibili.com/x/garb/user/preview/asset/list?"

def GenerateTraceID(time = buy_time):
    trace_id_uid = str(uuid.uuid4()).replace("-", "")[0:26].lower()
    trace_id_hex = hex(int(time / 256)).lower().replace("0x", "")
    trace_id = trace_id_uid + trace_id_hex + ":" + trace_id_uid[-10:] + trace_id_hex + ":0:0"
    return trace_id

trace_id = GenerateTraceID(buy_time)

def SessionDataAddMd5Sign(data_str):
    """ 计算sign并且在表单添加sign """
    md5_data = f"{data_str}{app_sec}"
    md5_ = hashlib.md5()
    md5_.update(md5_data.encode())
    sign = md5_.hexdigest()
    all_data = data_str + f"&sign={sign}"
    return all_data, str(len(all_data))

def GenerateSuitLockContent():
    """ 生成下单用表单 """
    statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
    statistics = statistics_.replace("__version__", version)
    data_str = urlencode({
        "access_key": access_key,
        "appkey": app_key,
        "csrf": csrf,
        "disable_rcmd": "0",
        "statistics": statistics,
        "ts": str(buy_time)
    })
    return SessionDataAddMd5Sign(data_str)

def GenerateSuitBuyContent(buy_num, add_month, item = item_id, time = buy_time):
    """ 生成下单用表单 """
    statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
    statistics = statistics_.replace("__version__", version)
    data_str = urlencode({
        "access_key": access_key, "add_month": add_month,
        "appkey": app_key, "buy_num": str(buy_num),
        "coupon_token": "", "csrf": csrf,
        "currency": "bp", "disable_rcmd": "0",
        "f_source": "shop", "from": "feed.card", "from_id": "",
        "item_id": str(item_id), "m_source": "",
        "platform": "android", "statistics": statistics,
        "ts": str(time)
    })
    return SessionDataAddMd5Sign(data_str)

def _win_set_time(time_tuple):
    import win32api as pywin32
    dayOfWeek = datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4], time_tuple[5], time_tuple[6]).isocalendar()[2]
    pywin32.SetSystemTime( time_tuple[0], time_tuple[1], dayOfWeek, time_tuple[2], time_tuple[3], time_tuple[4], time_tuple[5], time_tuple[6])

def _linux_set_time(time_tuple):
    import ctypes
    import ctypes.util
    import time

    CLOCK_REALTIME = 0

    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( datetime.datetime( *time_tuple[:6]).timetuple() ) )
    ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond

    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

def suitLock():
    data, length = GenerateSuitLockContent()
    lockHeader = {
        "Host":"api.bilibili.com",
        "native_api_from":"h5",
        "accept":"application/json, text/plain, */*",
        "referer":"https://www.bilibili.com/h5/mall/myasset",
        "content-type":"application/json",
        "env":"prod",
        "app-key":"android64",
        "user-agent":agent,
        "x-bili-trace-id":GenerateTraceID(),
        "x-bili-aurora-eid":eid,
        "x-bili-mid":uid,
        "x-bili-aurora-zone":"",
        "bili-bridge-engine":"cronet",
        "accept-encoding":"gzip, deflate"
    }
    r = requests.get(url = lock_url + data, cookies = cookies, headers = lockHeader)
    # print(r.text)

def adjustTime20():
    time_count = 0
    max = 10000
    sum = 0
    ave = 0
    while True:
        try:
            while time_count < 20:
                if(time_count == 0):
                    print("开始测试延迟误差...\n")
                time_timer = time.time()
                res = requests.get(url = time_url, headers = time_headers, timeout = 0.5)
                bili_time = float(eval(res.text)["data"]["splash_request_id"][0:13])
                d = bili_time - time_timer * 1000
                if d < max:
                    max = d
                time.sleep(0.2)
                time_count += 1
                sum += d
            if time_count != 0 and ave == 0:
                ave = sum / time_count / 1000
                print(ave * 1000)
                break
        except:
            print("计算误差异常")
            ave = 0
            break
    try:
        time_tuple = [2022, 8, 28, 11, 0, 0, 0]
        timeStamp = time.time() + ave
        dateArray = str(datetime.datetime.utcfromtimestamp(timeStamp))
        # print(dateArray)
        # print("\n")

        time_tuple[0] = int(dateArray[0:4])
        time_tuple[1] = int(dateArray[5:7])
        time_tuple[2] = int(dateArray[8:10])
        time_tuple[3] = int(dateArray[11:13])
        time_tuple[4] = int(dateArray[14:16])
        time_tuple[5] = int(dateArray[17:19])
        time_tuple[6] = int(dateArray[20:23])

        if sys.platform=='linux2':
            _linux_set_time(time_tuple)
        elif  sys.platform=='win32':
            _win_set_time(time_tuple)
        # os.system("pause")
    except:
        print("时间设置失败")
    print("")

def adjustTime():
    time_count = 0
    max = 10000
    sum = 0
    ave = 0
    while True:
        try:
            while time.time() + 30.2 >= buy_time and time.time() + 10.2 < buy_time:
                if(time_count == 0):
                    print("开始测试延迟误差...\n")
                time_timer = time.time()
                res = requests.get(url = time_url, headers = time_headers, timeout = 0.5)
                bili_time = float(eval(res.text)["data"]["splash_request_id"][0:13])
                d = bili_time - time_timer * 1000
                if d < max:
                    max = d
                time.sleep(0.5)
                time_count += 1
                sum += d
            if time_count != 0 and ave == 0:
                ave = sum / time_count / 1000
                print(ave * 1000)
                break
        except:
            print("计算误差异常")
            ave = 0
            break
    try:
        time_tuple = [2022, 8, 28, 11, 0, 0, 0]
        timeStamp = time.time() + ave
        dateArray = str(datetime.datetime.utcfromtimestamp(timeStamp))
        # print(dateArray)
        # print("\n")

        time_tuple[0] = int(dateArray[0:4])
        time_tuple[1] = int(dateArray[5:7])
        time_tuple[2] = int(dateArray[8:10])
        time_tuple[3] = int(dateArray[11:13])
        time_tuple[4] = int(dateArray[14:16])
        time_tuple[5] = int(dateArray[17:19])
        time_tuple[6] = int(dateArray[20:23])

        if sys.platform=='linux2':
            _linux_set_time(time_tuple)
        elif  sys.platform=='win32':
            _win_set_time(time_tuple)
        # os.system("pause")
    except:
        print("时间设置失败")
    print("")

data, length = GenerateSuitBuyContent(buy_num, -1, item_id, buy_time)

headers = {
    "Host":"api.bilibili.com",
    "Connection": "keep-alive",
    "content-length":length,
    "native_api_from":"h5",
    "buvid":cookies["Buvid"],
    "accept":"application/json, text/plain, */*",
    "referer":f"https://www.bilibili.com/h5/mall/suit/detail?id={item_id}&navhide=1&f_source=shop&from=feed.card&from_id=",
    "content-type":"application/x-www-form-urlencoded; charset=utf-8",
    "env":"prod",
    "app-key":"android64",
    "user-agent":agent,
    "x-bili-trace-id":trace_id,
    "x-bili-aurora-eid":eid,
    "x-bili-mid":uid,
    "x-bili-aurora-zone":"",
    "bili-bridge-engine":"cronet",
    "accept-encoding":"gzip, deflate, br"
}


if time.time() > buy_time:
    print("\n抢购已过时\n")
    os.system("pause")
    sys.exit(0)
elif buy_time - time.time() > 40:
    adjustTime20()

print(f"item_id: {item_id} buy_num: {buy_num}")
try:
    name_res = requests.get(url = name_url, headers = header)
    my_name = json.loads(name_res.text)["data"]["name"]
    print(f"昵称: {my_name}")
except:
    print("昵称获取失败")
order_time = str(datetime.datetime.fromtimestamp(buy_time))
print(order_time)
print(time.time())
print(f"剩余时间: {int(buy_time - time.time())}秒")
print("\n等待抢购...\n")

# while True:
if local_timer:
    adjustTime()

while True:
    if time.time() - predict_time >= buy_time and local_timer:
        try:
            # t1 = time.time()
            # print("presspresspresspresspresspresspresspresspresspress\n")
            res = requests.post(url = url, data = data, headers = headers , cookies = cookies)
            # res = requests.get(url = time_url, headers = time_headers, timeout = 0.5)
            # bili_time = int(eval(res.text)["data"]["splash_request_id"][0:13])
            # print(bili_time - buy_time*1000, "ms")

            print(time.time())
            # suitLock()
            print("")
            print(res.text)
            print("\n抢购完成\n")
            os.system("pause")
            break
        except:
            print("异常")
            os.system("pause")
            break

    elif (not local_timer) and buy_time - time.time() <= 30:
        addr = ("127.0.0.1", 23333)
        addr = ("Moonkey233.top", 23333)
        # addr = ("82.157.116.115", 23333)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        print(f"{addr} 时间服务端连接成功")
        sale_time = str(buy_time*1000)
        s.send(sale_time.encode('utf-8')) # 发消息
        print(f"已发送购买时间: {sale_time}")

        while True:
        # session = requests.session()
        # session.get(url="https://app.bilibili.com/x/v2/splash/show")
            msg = int(s.recv(1024).decode("utf-8", "ingore"))
            if msg == 0:
                # print(msg)
                # print(time.time())
                # res = requests.get(url="https://app.bilibili.com/x/v2/splash/show")
                # t = int(json.loads(res.text)["data"]["splash_request_id"][0:13])
                # print(t)
                # print(t - int(sale_time), "ms")
                t = time.time()
                # print("\npresspresspresspresspresspresspresspresspresspress\n")
                res = requests.post(url = url, data = data, headers = headers , cookies = cookies)
                print(time.time() - t)
                suitLock()
                print(res.text)
                print("\n抢购完成\n")
                break
            elif msg == -1:
                print(msg)
                break
            else:
                continue

        s.close()
        os.system("pause")
        break
    # buy_time += 12
    # max = 10000
    # time_count = 0
    # sum = 0
    # ave = 0
# os.system("pause")
sys.exit(0)
