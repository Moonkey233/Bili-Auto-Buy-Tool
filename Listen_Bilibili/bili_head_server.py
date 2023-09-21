# Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright ? 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

from inspect import trace
import os
import sys
import time
import json
import uuid
import ctypes
import datetime
import hashlib
import requests
from urllib.parse import urlencode

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

#变化值
predict_time = 0.2 #负数提前, 正数延后, 单位: 秒
buy_num = 1 #购买套数m 建议大前期号为1, 至多2
item_id = 38223 #购买装扮id
# item_id = 32296 #test
uid = "403229204" #购买者uid
buy_time = 1663412400 #装扮开售标准时间
# buy_time = int(time.time() + 12)
version = "6.89.0" #抓包版本号
eid = "VVQCRFMNBFED" #有时效的用户登录验证, 抓包
csrf = "4fbf58a8b7dfc233d5c9a8817f1b29f4" #有时效的用户登录验证, 抓包
access_key = "006822f4f8e39f9ebd2469c1f2022891" #有时效的用户登录验证, 抓包
cookies = { #有时效的用户登录验证, 抓包
    "SESSDATA":"dd669c41%2C1678890913%2C482f2291",
    "DedeUserID__ckMd5":"a9c89f4ba15a3c66",
    "sid":"555i5y26",
    "Buvid":"XX57096569BE10B097E4EFB36850197D6460A",
    "bili_jct":csrf,
    "DedeUserID":uid
}
#有时效的用户登录验证, 抓包
agent = "Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 os/android model/Mi 10 Pro build/6890300 osVer/12 sdkInt/31 network/2 BiliApp/6890300 mobi_app/android channel/xiaomi Buvid/XX57096569BE10B097E4EFB36850197D6460A sessionID/9711c9f3 innerVer/6890310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.89.0 os/android model/Mi 10 Pro mobi_app/android build/6890300 channel/xiaomi innerVer/6890310 osVer/12 network/2"
api_cookie = r'''buvid3=DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc; i-wanna-go-back=-1; _uuid=B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc; buvid4=5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==; buvid_fp_plain=undefined; buvid_fp=12ec06c99d3813205d1bd6fc4978b706; rpdid=|(J~JY|YuRY~0J'uYR~k~lkYY; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5516474282866283; nostalgia_conf=-1; blackside_state=0; hit-dyn-v2=1; CURRENT_QUALITY=120; bp_video_offset_416166928=697567164921544800; bp_video_offset_215177187=697895274748575900; fingerprint3=3f1b7a30861b19380f9fd5561f012e65; bp_video_offset_392774666=698945677744406500; is-2022-channel=1; fingerprint=5f9964bfeda77c7caa29037eff00c242; b_nut=100; DedeUserID=1709355263; DedeUserID__ckMd5=22a2d87c4842710c; b_ut=5; PVID=1; CURRENT_FNVAL=4048; SESSDATA=dedea7f2,1678711301,50936*91; bili_jct=a3d0eb37dccec85889271d757e9fcfb7; sid=7dqt6br6; innersign=0; b_lsid=310B5D7B6_183495B5980; bp_video_offset_1709355263=706710854100320300'''

header = {
    'user-agent':'Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 os/android model/Mi 10 Pro build/6890300 osVer/12 sdkInt/31 network/2 BiliApp/6890300 mobi_app/android channel/xiaomi Buvid/XX57096569BE10B097E4EFB36850197D6460A sessionID/9711c9f3 innerVer/6890310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.89.0 os/android model/Mi 10 Pro mobi_app/android build/6890300 channel/xiaomi innerVer/6890310 osVer/12 network/2',
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': api_cookie
} #cookie也要抓

time_headers = { #app开屏抓包获取时间戳
    "Host": "app.bilibili.com",
    # "buvid": "XX185A1175A6B2CC78AC6AC2FDB57813F6EE1",
    # "fp_local": "6f278567b657892765005bd9b88a4eda20220522214303312ae53b481d83b025",
    # "fp_remote": "6f278567b657892765005bd9b88a4eda20220522214303312ae53b481d83b025",
    # "session_id": "4cc23ed8",
    "env": "prod",
    "app-key": "android64",
    "user-agent": "Mozilla/5.0 BiliDroid/6.86.0 (bbcallen@gmail.com) os/android model/Mi 10 mobi_app/android build/6860300 channel/xiaomi innerVer/6860310 osVer/12 network/2",
    # "x-bili-trace-id": "e3635590b4d3c0376dbac1eb8f63079e:6dbac1eb8f63079e:0:0",
    # "x-bili-aurora-eid": "U1QDT1MGDlYDWw==",
    # "x-bili-mid": "2029228747",
    "x-bili-aurora-zone": "",
    "bili-bridge-engine": "cronet",
    "accept-encoding": "gzip, deflate"
}
# time_data = r'''access_key=8771d385aa1ece7bec6b3d1ae6302f81&ad_extra=E86F4CFF1F8FA890A75155EEAA51E6AE4FA9DBE62FCE708186D0CE5EF37B86948620D8BA1D991685B1288E2EDE09C6D52F8C2D33D59872EAE1EB776D11F71523CE1AF2112D8A950B98F6A1A48F848BC6D87798042220B2A8701CE4CAE188B48E0C10C96B4FB316E95A4F122758406A730408723357E030E938B6CA680A7ECB1B9DB4E436149FAE8CE62C95EB86F4D6A425F0FDC442004FBFC0AAAC0801E1839BBCC1BC0E9A983474B5E3F5AFA17DCD0D0226E53D87A8318B1FD0A842CC6A4C6F82165EF2BF00534A7E1B72D965CD2A5F65BDB3286967378BEA659646556020B050749322A909CBC2317699A978C567F9FABA2F8F7B7E58E4364467F6B32B5D639384CA64683B68931471C3FA7F7AC86BB465F0711DCE2B7CA23933391F271A4240D60A30EE6092638E70E062D9F4B3911146DF83E4C07C74FCF9EFFF15C6BED6291EC477C52E2C4A33A9BFB09E61DC55EF16C1D89EA19AC948E0E9FA775FF93C1249EFC2E819D29500E98B73971DF93607E55CD7D0D48AFECA0C1A81D64778E32C7271E32003610D68BFB74D606EC29D504FB14A095D80F30FB64E18165E1642AD68F22CF9FA2801D6439658BAFDCB077739B9C153C978941E0AD62AF19EF041209C9C06CBE671FD49D637271AAAD3B47364560D604F025B4C3F4EE3261A3DB07D50E637D9DE8332BB419D53B5CFAC9A6B6AC806A6DC867D7AB93FC9A17307011A645D2DA36F4187EDFF5C6EA3C462D4821D66B0A94C3BC85137CA0D550602493AD64806B6437BEB04729A2A02B5987233FD854C8ED34D92184F8F220739961980222CA6F62C0A9B3FA3B226E479FC1000098201AF9A7D0653AFDB07DF2D3DBEEC2CFB3389EA4581CB74A19D97DD189170E723B7FB9A061C655669A735651D1B0A05803BFA5D9DAFE8FD2AE4B57A76B0&appkey=1d8b6e7d45233436&birth=0101&build=6860300&c_locale=zh_CN&channel=xiaomi&disable_rcmd=0&height=2340&mobi_app=android&network=wifi&platform=android&s_locale=zh_CN&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.86.0%22%2C%22abtest%22%3A%22%22%7D&ts=1661443818&width=1080&sign=7a45a656e420a874bb35aea190c1bbd1'''

#不变值
app_key = "1d8b6e7d45233436"
app_sec = "560c52ccd288fed045859ed18bffd973"
url = "https://api.bilibili.com/x/garb/v2/trade/create"
time_url = "https://app.bilibili.com/x/v2/splash/show"
name_url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}'
lock_url = "https://api.bilibili.com/x/garb/user/preview/asset/list?"

def GenerateTraceID():
    trace_id_uid = str(uuid.uuid4()).replace("-", "")[0:26].lower()
    trace_id_hex = hex(int(buy_time / 256)).lower().replace("0x", "")
    trace_id = trace_id_uid + trace_id_hex + ":" + trace_id_uid[-10:] + trace_id_hex + ":0:0"
    return trace_id

trace_id = GenerateTraceID()
max = 10000
time_count = 0
sum = 0
ave = 0

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
        "ts": str(buy_time)
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
        "accept-encoding":"gzip, deflate, br"
    }
    r = requests.get(url = lock_url + data, cookies = cookies, headers = lockHeader)
    # print(r.text)


data, length = GenerateSuitBuyContent(buy_num, -1)

headers = {
    "Host":"api.bilibili.com",
    "content-length":length,
    "native_api_from":"h5",
    "accept":"application/json, text/plain, */*",
    "referer":f"https://www.bilibili.com/h5/mall/suit/detail?navhide=1&from=icon.category&id={item_id}&f_source=shop&native.theme=1",
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
if time.time() > buy_time:
    print("\n抢购已过时\n")
    os.system("pause")
    sys.exit(0)
print(f"剩余时间: {int(buy_time - time.time())}秒")
print("\n等待抢购...\n")

# while True:
while True:
    try:
        while time.time() + 10.2 >= buy_time and time.time() + 2.2 < buy_time:
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

while True:
    if time.time() - predict_time >= buy_time:
        try:
            # t1 = time.time()
            res = requests.post(url = url, data = data, headers = headers , cookies = cookies)
            # print(time.time() - t1)
            print(res.text)
            # if int(eval(res.text)["code"]) != 0:
            #     res = requests.post(url = url, data = data, headers = headers , cookies = cookies)
            #     print(res.text)
            suitLock()
            print("\n抢购完成\n")
            order_time = str(datetime.datetime.fromtimestamp(buy_time))
            print(order_time)
            with open("temp.txt", "w") as f:
                f.write(res.text)
                f.close()
            os.system("pause")
            break
        except:
            print("异常")
            pass
    # buy_time += 12
    # max = 10000
    # time_count = 0
    # sum = 0
    # ave = 0
sys.exit(0)
