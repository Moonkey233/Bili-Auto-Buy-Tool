import json
import requests
import os
import urllib.parse
import urllib.request
import time
import sys
import uuid
import hashlib
import requests
from urllib.parse import urlencode

#不变值
my_name = "" #设置购买用户名称
app_key = "1d8b6e7d45233436"
app_sec = "560c52ccd288fed045859ed18bffd973"

item_id = 6146
uid_bili = "392774666" #设置购买用户UID, 目前就显示用
#变化值
version = "6.88.0" #抓包版本号
eid = "Ul0DQVYAAFcB" #有时效的用户登录验证, 抓包
csrf = "c6a80c2c7fb69783bbc10aa7b7714a38" #有时效的用户登录验证, 抓包
access_key = "ef0a1f1797beb3aa7b57924b8bc14f91" #有时效的用户登录验证, 抓包
cookies = { #有时效的用户登录验证, 抓包
    "SESSDATA":"560154f6%2C1678421215%2C9805e691",
    "DedeUserID__ckMd5":"b0a7c64e70aeca8e",
    "sid":"71z8d9m0",
    "Buvid":"XX185A1175A6B2CC78AC6AC2FDB57813F6EE1",
    "bili_jct":csrf,
    "DedeUserID":uid_bili
}
#有时效的用户登录验证, 抓包
agent = "Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 os/android model/Mi 10 build/6880300 osVer/11 sdkInt/30 network/2 BiliApp/6880300 mobi_app/android channel/xiaomi Buvid/XX185A1175A6B2CC78AC6AC2FDB57813F6EE1 sessionID/82a9ce82 innerVer/6880310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.88.0 os/android model/Mi 10 mobi_app/android build/6880300 channel/xiaomi innerVer/6880310 osVer/11 network/2"

# num_url = f'https://api.bilibili.com/x/garb/order/item/count/unpaid?item_id={item_id}'
list_url = 'https://api.bilibili.com/x/garb/order/list?'
lock_url = "https://api.bilibili.com/x/garb/user/preview/asset/list?"

def SessionDataAddMd5Sign(data_str):
    """ 计算sign并且在表单添加sign """
    md5_data = f"{data_str}{app_sec}"
    md5_ = hashlib.md5()
    md5_.update(md5_data.encode())
    sign = md5_.hexdigest()
    all_data = data_str + f"&sign={sign}"
    return all_data

def GenerateSuitBuyContent():
    """ 生成下单用表单 """
    statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
    statistics = statistics_.replace("__version__", version)
    data_str = urlencode({
        "access_key": access_key,
        "appkey": app_key, "csrf": csrf,
        "disable_rcmd": "0","pn": "1", "state": "1",
        "statistics": statistics,
        "ts": str(round(time.time()))
    })
    return SessionDataAddMd5Sign(data_str)

def GenerateTraceID():
    trace_id_uid = str(uuid.uuid4()).replace("-", "")[0:26].lower()
    trace_id_hex = hex(int(round(time.time()) / 256)).lower().replace("0x", "")
    trace_id = trace_id_uid + trace_id_hex + ":" + trace_id_uid[-10:] + trace_id_hex + ":0:0"
    return trace_id

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
        "ts": str(int(time.time()))
    })
    return SessionDataAddMd5Sign(data_str)

def suitPost():
    data = GenerateSuitBuyContent()
    header = {
        "Host":"api.bilibili.com",
        # "content-length":length,
        "native_api_from":"h5",
        "accept":"application/json, text/plain, */*",
        "referer":f"https://www.bilibili.com/h5/mall/v2/order?navhide=1",
        "content-type":"application/json",
        "env":"prod",
        "app-key":"android64",
        "user-agent":agent,
        "x-bili-trace-id":GenerateTraceID(),
        "x-bili-aurora-eid":eid,
        "x-bili-mid":uid_bili,
        "x-bili-aurora-zone":"",
        "bili-bridge-engine":"cronet",
        "accept-encoding":"gzip, deflate, br"
    }
    # print(list_url + "?" + data)
    res = requests.get(url = list_url + data, headers = header , cookies = cookies)
    print(json.loads(res.text)["data"]["page"]["total"])

def suitLock():
    data = GenerateSuitLockContent()
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
        "x-bili-mid":uid_bili,
        "x-bili-aurora-zone":"",
        "bili-bridge-engine":"cronet",
        "accept-encoding":"gzip, deflate, br"
    }
    print(requests.get(url = lock_url + data, cookies = cookies, headers = lockHeader).text)

while True:
    suitLock()
    os.system("pause")
    # time.sleep(0.1)
