import json
import os
import ctypes, sys
import time
import datetime
import requests

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

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

max = 10000
time_count = 0
sum = 0
ave = 0

time_url = "https://app.bilibili.com/x/v2/splash/show"
time_headers = { #app开屏抓包获取时间戳
    "Host": "app.bilibili.com",
    # "buvid": "XX185A1175A6B2CC78AC6AC2FDB57813F6EE1",
    # "fp_local": "6f278567b657892765005bd9b88a4eda20220522214303312ae53b481d83b025",
    # "fp_remote": "6f278567b657892765005bd9b88a4eda20220522214303312ae53b481d83b025",
    # "session_id": "4cc23ed8",
    "env": "prod",
    "app-key": "android64",
    "user-agent": "Mozilla/5.0 BiliDroid/6.89.0 (bbcallen@gmail.com) os/android model/Mi 10 mobi_app/android build/6890300 channel/xiaomi innerVer/6890310 osVer/12 network/2",
    # "x-bili-trace-id": "e3635590b4d3c0376dbac1eb8f63079e:6dbac1eb8f63079e:0:0",
    # "x-bili-aurora-eid": "U1QDT1MGDlYDWw==",
    # "x-bili-mid": "2029228747",
    "x-bili-aurora-zone": "",
    "bili-bridge-engine": "cronet",
    "accept-encoding": "gzip, deflate"
}

time.sleep(1)
null = ""
true = True
false = False
while True:
    try:
        session = requests.Session()
        # while True:
        while time_count < 20:
            if(time_count == 0):
                print("开始测试延迟误差...\n")
            time_timer = time.time()
            res = session.get(url = time_url)
            # print((time.time() - time_timer))
            bili_time = float(json.loads(res.text)["data"]["splash_request_id"][0:13])
            # print(time_count)
            d = bili_time - time_timer * 1000
            if d < max:
                max = d
            time.sleep(0.2)
            time_count += 1
            sum += d
        session.close()
        if time_count != 0 and ave == 0:
            ave = sum / time_count / 1000
            print(ave*1000)
            break
    except Exception as e:
        print("计算误差异常")
        print(str(e))
        ave = 0
        break

time_tuple = [2022, 8, 27, 11, 0, 0, 0]

timeStamp = time.time() + ave

dateArray = str(datetime.datetime.utcfromtimestamp(timeStamp))
print(dateArray)

time_tuple[0] = int(dateArray[0:4])
time_tuple[1] = int(dateArray[5:7])
time_tuple[2] = int(dateArray[8:10])
time_tuple[3] = int(dateArray[11:13])
time_tuple[4] = int(dateArray[14:16])
time_tuple[5] = int(dateArray[17:19])
time_tuple[6] = int(dateArray[20:23])

print(time_tuple)

if sys.platform=='linux2':
    _linux_set_time(time_tuple)
elif  sys.platform=='win32':
    _win_set_time(time_tuple)

print(time.time())
os.system("pause")