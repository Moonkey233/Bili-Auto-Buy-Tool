import os
import ctypes, sys
import time
import datetime
import requests
from urllib.parse import urlencode

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
# time_data = r'''access_key=8771d385aa1ece7bec6b3d1ae6302f81&ad_extra=E86F4CFF1F8FA890A75155EEAA51E6AE4FA9DBE62FCE708186D0CE5EF37B86948620D8BA1D991685B1288E2EDE09C6D52F8C2D33D59872EAE1EB776D11F71523CE1AF2112D8A950B98F6A1A48F848BC6D87798042220B2A8701CE4CAE188B48E0C10C96B4FB316E95A4F122758406A730408723357E030E938B6CA680A7ECB1B9DB4E436149FAE8CE62C95EB86F4D6A425F0FDC442004FBFC0AAAC0801E1839BBCC1BC0E9A983474B5E3F5AFA17DCD0D0226E53D87A8318B1FD0A842CC6A4C6F82165EF2BF00534A7E1B72D965CD2A5F65BDB3286967378BEA659646556020B050749322A909CBC2317699A978C567F9FABA2F8F7B7E58E4364467F6B32B5D639384CA64683B68931471C3FA7F7AC86BB465F0711DCE2B7CA23933391F271A4240D60A30EE6092638E70E062D9F4B3911146DF83E4C07C74FCF9EFFF15C6BED6291EC477C52E2C4A33A9BFB09E61DC55EF16C1D89EA19AC948E0E9FA775FF93C1249EFC2E819D29500E98B73971DF93607E55CD7D0D48AFECA0C1A81D64778E32C7271E32003610D68BFB74D606EC29D504FB14A095D80F30FB64E18165E1642AD68F22CF9FA2801D6439658BAFDCB077739B9C153C978941E0AD62AF19EF041209C9C06CBE671FD49D637271AAAD3B47364560D604F025B4C3F4EE3261A3DB07D50E637D9DE8332BB419D53B5CFAC9A6B6AC806A6DC867D7AB93FC9A17307011A645D2DA36F4187EDFF5C6EA3C462D4821D66B0A94C3BC85137CA0D550602493AD64806B6437BEB04729A2A02B5987233FD854C8ED34D92184F8F220739961980222CA6F62C0A9B3FA3B226E479FC1000098201AF9A7D0653AFDB07DF2D3DBEEC2CFB3389EA4581CB74A19D97DD189170E723B7FB9A061C655669A735651D1B0A05803BFA5D9DAFE8FD2AE4B57A76B0&appkey=1d8b6e7d45233436&birth=0101&build=6860300&c_locale=zh_CN&channel=xiaomi&disable_rcmd=0&height=2340&mobi_app=android&network=wifi&platform=android&s_locale=zh_CN&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.86.0%22%2C%22abtest%22%3A%22%22%7D&ts=1661443818&width=1080&sign=7a45a656e420a874bb35aea190c1bbd1'''
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

while True:
    try:
        while time_count < 20:
            if(time_count == 0):
                print("开始测试延迟误差...\n")
            time_timer = time.time()
            # print(time_timer)
            res = requests.get(url = time_url, headers = time_headers, timeout = 0.5)
            # print(res.text)
            bili_time = float(eval(res.text)["data"]["splash_request_id"][0:13])
            # print(bili_time)
            d = bili_time - time_timer * 1000
            if d < max:
                max = d
            time.sleep(0.2)
            time_count += 1
            sum += d
        if time_count != 0 and ave == 0:
            ave = sum / time_count / 1000
            print(ave*1000)
            break
    except:
        print("计算误差异常")
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