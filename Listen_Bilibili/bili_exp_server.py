# Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright © 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

import os
import sys
import time
import json
import uuid
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import hashlib
import requests
from urllib.parse import urlencode

# tt = 0

#变化值
buy_num = 12 #设置购买秒杀套数1-100
uid_bili = "392774666" #设置购买用户UID, 目前就显示用
expectation = 1314 #设置预期抢购的编号
final_num = 2 #设置最终区间 1314 2 即代表播报1311触发最后连号
item_id = 38223 #设置监听装扮id, 断网或抓包获得网址后网页调试获得
fresh_sec = 0.1 #设置刷新的间隔
# fresh_sec2 = 0.1 #设置100套内刷新的间隔
mail_on = True #设置邮件提示开启
deviation_predict = 0 #设置预判偏移量, 0或一个正整数, 慎用
# mail_num = 500 #设置邮件提前提醒数量
receiver = ['3422180797@qq.com', 'Moonkey233@foxmail.com'] #设置通知接受邮箱地址
version = "6.89.0" #抓包版本号
eid = "Ul0DQVYAAFcB" #有时效的用户登录验证, 抓包
csrf = "b575516c280189bc39147bdc9dd02eb2" #有时效的用户登录验证, 抓包
access_key = "505893d7fd648c22d7649ccef9404491" #有时效的用户登录验证, 抓包
cookies = { #有时效的用户登录验证, 抓包
    "SESSDATA":"44fc4c80%2C1678959741%2Cd4751591",
    "DedeUserID__ckMd5":"b0a7c64e70aeca8e",
    "sid":"dwyx3u1s",
    "Buvid":"XU98BFE91484E940286674C84ADBAED4054B7",
    "bili_jct":csrf,
    "DedeUserID":uid_bili
}
#有时效的用户登录验证, 抓包
agent = "Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 os/android model/Mi 10 Pro build/6890300 osVer/12 sdkInt/31 network/2 BiliApp/6890300 mobi_app/android channel/xiaomi Buvid/XU98BFE91484E940286674C84ADBAED4054B7 sessionID/d7e89c52 innerVer/6890310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.89.0 os/android model/Mi 10 Pro mobi_app/android build/6890300 channel/xiaomi innerVer/6890310 osVer/12 network/2"
api_cookie = r'''buvid3=DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc; i-wanna-go-back=-1; _uuid=B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc; buvid4=5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==; buvid_fp_plain=undefined; buvid_fp=12ec06c99d3813205d1bd6fc4978b706; rpdid=|(J~JY|YuRY~0J'uYR~k~lkYY; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5516474282866283; nostalgia_conf=-1; blackside_state=0; hit-dyn-v2=1; CURRENT_QUALITY=120; bp_video_offset_416166928=697567164921544800; bp_video_offset_215177187=697895274748575900; fingerprint3=3f1b7a30861b19380f9fd5561f012e65; bp_video_offset_392774666=698945677744406500; is-2022-channel=1; fingerprint=5f9964bfeda77c7caa29037eff00c242; b_nut=100; DedeUserID=1709355263; DedeUserID__ckMd5=22a2d87c4842710c; b_ut=5; PVID=1; CURRENT_FNVAL=4048; SESSDATA=dedea7f2,1678711301,50936*91; bili_jct=a3d0eb37dccec85889271d757e9fcfb7; sid=7dqt6br6; bp_video_offset_1709355263=706710854100320300'''

#初始化变量参数
null = ""
winner = ""
item_name = ""
num = 0
number = 0
true_buy_num = 0
lastest_id = 0
timer = 0
bad_net = 0
true_number = 0
host_server = 'smtp.qq.com'
sender_qq = 'Moonkey_Work@foxmail.com'
pwd = 'nsjwkzmtikncbibf'
url = f'https://api.bilibili.com/x/garb/v2/mall/suit/detail?from=&from_id=&item_id={item_id}&part=suit'
url2 = f'https://api.bilibili.com/x/garb/rank/fan/recent?item_id={item_id}'
name_url = f'https://api.bilibili.com/x/space/acc/info?mid={uid_bili}'
buy_url = "https://api.bilibili.com/x/garb/v2/trade/create"
header = {
    'user-agent': agent,
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': api_cookie
}

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
    "accept-encoding": "gzip, deflate, br"
}
# time_data = r'''access_key=8771d385aa1ece7bec6b3d1ae6302f81&ad_extra=E86F4CFF1F8FA890A75155EEAA51E6AE4FA9DBE62FCE708186D0CE5EF37B86948620D8BA1D991685B1288E2EDE09C6D52F8C2D33D59872EAE1EB776D11F71523CE1AF2112D8A950B98F6A1A48F848BC6D87798042220B2A8701CE4CAE188B48E0C10C96B4FB316E95A4F122758406A730408723357E030E938B6CA680A7ECB1B9DB4E436149FAE8CE62C95EB86F4D6A425F0FDC442004FBFC0AAAC0801E1839BBCC1BC0E9A983474B5E3F5AFA17DCD0D0226E53D87A8318B1FD0A842CC6A4C6F82165EF2BF00534A7E1B72D965CD2A5F65BDB3286967378BEA659646556020B050749322A909CBC2317699A978C567F9FABA2F8F7B7E58E4364467F6B32B5D639384CA64683B68931471C3FA7F7AC86BB465F0711DCE2B7CA23933391F271A4240D60A30EE6092638E70E062D9F4B3911146DF83E4C07C74FCF9EFFF15C6BED6291EC477C52E2C4A33A9BFB09E61DC55EF16C1D89EA19AC948E0E9FA775FF93C1249EFC2E819D29500E98B73971DF93607E55CD7D0D48AFECA0C1A81D64778E32C7271E32003610D68BFB74D606EC29D504FB14A095D80F30FB64E18165E1642AD68F22CF9FA2801D6439658BAFDCB077739B9C153C978941E0AD62AF19EF041209C9C06CBE671FD49D637271AAAD3B47364560D604F025B4C3F4EE3261A3DB07D50E637D9DE8332BB419D53B5CFAC9A6B6AC806A6DC867D7AB93FC9A17307011A645D2DA36F4187EDFF5C6EA3C462D4821D66B0A94C3BC85137CA0D550602493AD64806B6437BEB04729A2A02B5987233FD854C8ED34D92184F8F220739961980222CA6F62C0A9B3FA3B226E479FC1000098201AF9A7D0653AFDB07DF2D3DBEEC2CFB3389EA4581CB74A19D97DD189170E723B7FB9A061C655669A735651D1B0A05803BFA5D9DAFE8FD2AE4B57A76B0&appkey=1d8b6e7d45233436&birth=0101&build=6860300&c_locale=zh_CN&channel=xiaomi&disable_rcmd=0&height=2340&mobi_app=android&network=wifi&platform=android&s_locale=zh_CN&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.86.0%22%2C%22abtest%22%3A%22%22%7D&ts=1661443818&width=1080&sign=7a45a656e420a874bb35aea190c1bbd1'''

#不变值
my_name = "" #设置购买用户名称
app_key = "1d8b6e7d45233436"
app_sec = "560c52ccd288fed045859ed18bffd973"

def GenerateTraceID():
    trace_id_uid = str(uuid.uuid4()).replace("-", "")[0:26].lower()
    trace_id_hex = hex(int(round(time.time()) / 256)).lower().replace("0x", "")
    trace_id = trace_id_uid + trace_id_hex + ":" + trace_id_uid[-10:] + trace_id_hex + ":0:0"
    return trace_id

def send_mail(title, mail_content):
    try:
        mail_title = item_name + title
        msg = MIMEMultipart()
        msg["Subject"] = Header(mail_title,'utf-8')
        msg["From"] = sender_qq
        msg['To'] = ";".join(receiver)
        msg.attach(MIMEText(mail_content,'plain','utf-8'))
        smtp = SMTP_SSL(host_server)
        smtp.login(sender_qq,pwd)
        smtp.sendmail(sender_qq,receiver,msg.as_string())
        smtp.quit()
        print(title + " 邮件发送成功")
    except:
        print("邮件发送异常")

def SessionDataAddMd5Sign(data_str):
    """ 计算sign并且在表单添加sign """
    md5_data = f"{data_str}{app_sec}"
    md5_ = hashlib.md5()
    md5_.update(md5_data.encode())
    sign = md5_.hexdigest()
    all_data = data_str + f"&sign={sign}"
    return all_data, str(len(all_data))

def GenerateSuitBuyContent(n, add_month = -1):
    """ 生成下单用表单 """
    statistics_ = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
    statistics = statistics_.replace("__version__", version)
    data_str = urlencode({
        "access_key": access_key, "add_month": add_month,
        "appkey": app_key, "buy_num": str(n),
        "coupon_token": "", "csrf": csrf,
        "currency": "bp", "disable_rcmd": "0",
        "f_source": "shop", "from": "icon.category", "from_id": "",
        "item_id": str(item_id),
        "platform": "android", "statistics": statistics,
        "ts": str(round(time.time()))
    })
    return SessionDataAddMd5Sign(data_str)

def suitPost(n):
    data, length = GenerateSuitBuyContent(n, -1)
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
        "x-bili-trace-id":GenerateTraceID(),
        "x-bili-aurora-eid":eid,
        "x-bili-mid":uid_bili,
        "x-bili-aurora-zone":"",
        "bili-bridge-engine":"cronet",
        "accept-encoding":"gzip, deflate, br"
    }
    res = requests.post(url = buy_url, data = data, headers = headers , cookies = cookies)
    print(res.text)

if __name__ == "__main__":
    '''主函数'''
    while True:
        #刷新请求申请
        if time.time() - timer > fresh_sec:
            # print(time.time() - tt)
            # tt = time.time()
            try:

                reponse2 = requests.get(url = url2, headers = header)
                number = json.loads(reponse2.text)["data"]["rank"][0]["number"]
                true_number = number if number >= lastest_id else lastest_id

                # print(true_number)

                #爬虫请求
                if timer == 0:
                    name_res = requests.get(url = name_url, headers = header)
                    my_name = json.loads(name_res.text)["data"]["name"]
                    reponse = requests.get(url = url, headers = header)
                    dic = json.loads(reponse.text)
                    item_name = dic["data"]["name"]
                    num = dic["data"]["sale_surplus"]
                    print("\n开始监听..." + "\n装扮名: " + item_name + 
                        "\n库存: " + str(num) + 
                        "\n当前编号: " + str(true_number) + 
                        "\n预期: " + str(expectation) + 
                        "\n抢购套数: " + str(buy_num) + 
                        "\n预期偏移修正量: "+ str(deviation_predict) + 
                        "\n实际范围: " + str(expectation - deviation_predict - buy_num) + " - " + str(expectation - final_num - 1) +
                        "\n剩余间隔: " + str(expectation - true_number - buy_num - deviation_predict) + 
                        "\n时间戳: " + str(time.time()) + 
                        "\n时间: " + time.asctime() +
                        "\nID: " + my_name)
                
                

                if true_number + buy_num + deviation_predict >= expectation and true_number + final_num + 1 <= expectation:
                    
                    true_buy_num = buy_num
                    # if buy_num % 10 != 0:
                    #     suitPost(buy_num % 10)
                    # while buy_num >= 10:
                    #     suitPost(10)
                    #     buy_num -= 10
                    suitPost(6)
                    suitPost(6)

                    #发起购买连号请求
                    # os.system(cmd)
                    # true_buy_num = expectation - true_number
                    # if true_buy_num <= 10:
                    #     suitPost(true_buy_num)
                    #     # pass
                    # else:
                    #     true_buy_num = buy_num
                    #     suitPost(buy_num % 10)
                    #     while buy_num > 10:
                    #         suitPost(10)
                    #         buy_num -= 10
                    #     # suitPost(buy_num)
                    # buy_num = -10000 #要不要发起重复订单?
                            
                    print("\n已发送购买请求..." + "\n装扮名: " + item_name + "\n智能购买套数: " + str(true_buy_num) + "\n时间戳: " + str(time.time()) + "\n时间: " + time.asctime())
                if bad_net > 0:
                    print("\n已恢复网络连接")
                    bad_net = 0

            except:
                bad_net += 1
                if bad_net <= 5:
                    print("网络异常, 第 " + str(bad_net) + "/5 次尝试失败...")
                elif bad_net == 6:
                    print("网络异常。请检查网络并重启, 若仍不能解决请更换IP或15分钟后再试, 请联系开发者")

            #发生新的购买记录
            lastest_id = number if number > lastest_id else lastest_id
            # if lastest_id < number:

            #     lastest_id = number
                # 邮件通知
                # if mail_on and expectation - true_number - 1 <= mail_num and expectation - true_number - 1 > mail_num - 10:
                #     send_mail("预期临近通知", "您监听的B站装扮 " + item_name + " 第(" + str(true_number) + ")套已被购买, 距预期(" + str(expectation) + ")仅间隔 【" + str(expectation - true_number - 1) + "】 套, 请留意购买。")

            #更新计时器
            timer = time.time()

        # 抢购结束
        if true_number + 1 > expectation:

            print("\n结束监听..." + "\n时间戳: " + str(time.time()) + "\n时间: " + time.asctime())

            try:

                reponse2 = requests.get(url = url2, headers = header)
                data2 = reponse2.text
                dic2 = json.loads(data2)

                for i in dic2["data"]["rank"]:
                    if i["nickname"] == my_name:
                        print("\n检测到最后购买编号播报: " + str(i["number"]) + "\n时间戳: " + str(time.time()) + "\n时间: " + time.asctime())
                        break

                winner = "未知, 请前往B站客户端检查是否抢购成功。"

                for i in dic2["data"]["rank"]:
                    if int(i["number"]) == expectation:
                        winner = i["nickname"]
                        
            except:
                print("查询预期编号拥有者失败")

            #邮件配置与发送
            if mail_on:
                isWin = ""
                if winner == my_name:
                    isWin = ", 恭喜您抢购成功!"
                send_mail("抢购结束通知", "您监听的B站装扮 " + item_name + " 预期编号【" + str(expectation) + "】抢购结束, 编号拥有者: " + winner + " 抢购套数: " + str(true_buy_num) + isWin)
            os.system("pause")
            sys.exit(0)