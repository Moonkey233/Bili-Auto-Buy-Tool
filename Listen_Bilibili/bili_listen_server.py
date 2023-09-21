# Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright © 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

import time
import json
import requests
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

item_list = [
    37941,
    37745,
    37813,
    37825,
    32296,
    4019,
    2010,
    33372,
    2554,
    3186,
    5359,
    3717,
    3637,
    4755,
    34805,
    34077,
    3796,
    37594,
    4150,
    4389,
    1911,
    2097,
    3638,
    4555,
    5128,
    33998,
    3556,
    3242,
    4259,
    5267,
    4447,
    4089,
    3054,
    2646,
    2725,
    2479,
    5766,
    35906,
    6208,
    2794,
    5829,
    34358,
    2109,
    5458,
    5392,
    1855,
    4666,
    3745,
    6469,
    32658,
    2890,
    34312,
    6052,
    6146,
    6086,
    32445,
    33832,
    37644,
    4756,
    4874,
    1648,
    5333,
    6518,
    6475,
    5424,
    33432,
    3952,
    5540,
    34031,
    5927,
    5957,
    35044,
    6572,
    6386,
    4800,
    34475,
    5797,
    1140,
    32709,
    3908,
    35609,
    3468,
    36177,
    34616,
    2180,
    33462,
    4696,
    4749,
    34377,
    37705,
    34025,
    32251,
    3055,
    6416,
    33801,
    34435,
    32891,
    34444,
    32692,
    33324,
    6334,
    33397,
    37153,
    36438,
    35943,
    6145,
    36426,
    34586,
    34255,
    37243,
    1157,
    33975,
    33627,
    33154,
    4873,
    33024,
    37126,
    32833,
    37213,
    36739,
    32611,
    6023,
    33626,
    4228,
    5301,
    32946,
    6293,
    5869,
    35543,
    36391,
    36352,
    36189,
    34701,
    34878,
    32482,
    35169,
    4200,
    32583,
    33323,
    6092,
    33972,
    33528,
    2845,
    1710,
    35755,
    3496,
    35849,
    37183,
    1410,
    34746,
    5235,
    35729,
    2059,
    33325,
    34024,
    33960,
    6548,
    4411,
    3500,
    37483,
    6230,
    3371,
    34068,
    35197,
    32546,
    32913,
    4002,
    2595,
    36785,
    35175,
    6298,
    34026,
    32608,
    32504,
    5719,
    33957,
    34281,
    35821,
    33182,
    36145,
    33838,
    1463,
    5679,
    37332,
    1685,
    37670,
    34100,
    1222,
    35705,
    3407,
    34895,
    37428,
    33344,
    37785,
    5747,
    34541,
    36039,
    32807,
    33108,
    34474,
    1704,
    35780,
    34151,
    32691,
    5995,
    33559,
    3582,
    32499,
    32345,
    37358,
    37388,
    36248,
    36012,
    35171,
    34747,
    34371,
    36115,
    35971,
    36283,
    34736,
    32916,
    35574,
    33250,
    35018,
    35645,
    35672,
    2979,
    32808,
    34984,
    34929,
    34584,
    37093,
    35551,
    37570,
    35550,
    37448,
    36083,
    36818,
    35545,
    35549,
    35868,
    35537,
    35544,
    36600,
    35554,
    35547,
    37542,
    35548,
    35552,
    35553
]

fav_list = [ #收藏特殊监听
    32296,
    37745,
    3717,
    4019,
    36352,
    37785,
    37825
]
round_range = 500 #临近靓号监听范围
all_listen_time = 43200 #多少秒监听一次全部装扮并发邮件 21600 6h
fav_listen_time = 60 #多少秒监听一次全部装扮并显示
# receiver = ['Moonkey233@foxmail.com', '2567519051@qq.com', '3422180797@qq.com'] #设置通知接受邮箱地址
receiver = ['Moonkey233@foxmail.com'] #设置通知接受邮箱地址
mail_on = True
json_on = True

return_list = []
ending_list = []
good_list = []
display_list = []

host_server = 'smtp.qq.com'
sender_qq = 'Moonkey_Work@foxmail.com'
pwd = 'nsjwkzmtikncbibf'
url = 'https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf=495347a5e1ff372a0b7c558af50bfa87&from=&from_id=&item_id=Moon&part=suit'
url2 = 'https://api.bilibili.com/x/garb/rank/fan/recent?csrf=495347a5e1ff372a0b7c558af50bfa87&item_id=Moon'
headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 12; Mi 10 Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.78 Mobile Safari/537.36 os/android model/Mi 10 build/6840300 osVer/12 sdkInt/31 network/2 BiliApp/6840300 mobi_app/android channel/xiaomi Buvid/XX185A1175A6B2CC78AC6AC2FDB57813F6EE1 sessionID/80031f98 innerVer/6840310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.84.0 os/android model/Mi 10 mobi_app/android build/6840300 channel/xiaomi innerVer/6840310 osVer/12 network/2',
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': r'''buvid3=CD12D3E0-0154-994C-BB04-EF33A88F73D563625infoc; b_nut=1669198663; i-wanna-go-back=-1; _uuid=433B91104-DBA5-8810B-410B7-C1B3E9EC2101D64146infoc; buvid_fp=0d7e32085e8946dab5a42296024183fc; buvid4=52C6D572-CDF7-6301-FC52-81560B34098565456-022112318-M3Jk972H7pGyInMc0Nuurg==; SESSDATA=8c98344f,1684750695,cccce*b1; bili_jct=a2379ae01dd30a16ab40fd2385a80986; DedeUserID=215177187; DedeUserID__ckMd5=db23a7f040ba3d37; b_ut=5; CURRENT_FNVAL=4048; rpdid=|(k|k~m~kkmJ0J'uYYmum)~l); nostalgia_conf=-1; LIVE_BUVID=AUTO5316695310809133; PVID=1; hit-new-style-dyn=0; hit-dyn-v2=1; fingerprint=76b536649ecf8d2695121faa02c2970b; CURRENT_QUALITY=120; bp_video_offset_215177187=743979105700020200'''
}

def isRound(n, num):
    if num - n > 0 and num - n <= round_range:
        return 1
    else:
        return 0

def isGoodNumber(n):
    temp = 0
    temp += isRound(n, 666)
    temp += isRound(n, 888)
    temp += isRound(n, 1000)
    temp += isRound(n, 1111)
    temp += isRound(n, 1234)
    temp += isRound(n, 2000)
    temp += isRound(n, 2222)
    temp += isRound(n, 2333)
    temp += isRound(n, 3333)
    temp += isRound(n, 4444)
    temp += isRound(n, 5555)
    temp += isRound(n, 6666)
    temp += isRound(n, 7777)
    temp += isRound(n, 8888)
    temp += isRound(n, 10000)
    temp += isRound(n, 11111)
    temp += isRound(n, 12345)
    temp += isRound(n, 13333)
    temp += isRound(n, 14444)
    temp += isRound(n, 15555)
    temp += isRound(n, 16666)
    temp += isRound(n, 17777)
    temp += isRound(n, 18888)
    temp += isRound(n, 20000)
    temp += isRound(n, 22222)
    temp += isRound(n, 23333)
    temp += isRound(n, 26666)
    temp += isRound(n, 28888)
    temp += isRound(n, 30000)
    temp += isRound(n, 33333)
    temp += isRound(n, 36666)
    temp += isRound(n, 38888)
    temp += isRound(n, 40000)
    temp += isRound(n, 43210)
    temp += isRound(n, 44444)
    temp += isRound(n, 46666)
    temp += isRound(n, 48888)
    temp += isRound(n, 50000)
    temp += isRound(n, 52000)
    temp += isRound(n, 54321)
    temp += isRound(n, 55555)
    temp += isRound(n, 56666)
    temp += isRound(n, 58888)
    temp += isRound(n, 60000)
    temp += isRound(n, 66666)
    temp += isRound(n, 68888)
    temp += isRound(n, 70000)
    temp += isRound(n, 76666)
    temp += isRound(n, 77777)
    temp += isRound(n, 78888)
    temp += isRound(n, 80000)
    temp += isRound(n, 86666)
    temp += isRound(n, 88888)
    temp += isRound(n, 90000)
    temp += isRound(n, 100000)
    temp += isRound(n, 111111)
    temp += isRound(n, 114514)
    temp += isRound(n, 122222)
    temp += isRound(n, 123456)
    temp += isRound(n, 131420)
    temp += isRound(n, 133333)
    temp += isRound(n, 144444)
    temp += isRound(n, 155555)
    temp += isRound(n, 166666)
    temp += isRound(n, 177777)
    temp += isRound(n, 188888)
    temp += isRound(n, 200000)
    temp += isRound(n, 211111)
    temp += isRound(n, 222222)
    temp += isRound(n, 233333)
    temp += isRound(n, 244444)
    temp += isRound(n, 255555)
    temp += isRound(n, 266666)
    temp += isRound(n, 277777)
    temp += isRound(n, 288888)
    temp += isRound(n, 300000)
    temp += isRound(n, 311111)
    temp += isRound(n, 322222)
    temp += isRound(n, 333333)
    temp += isRound(n, 344444)
    temp += isRound(n, 355555)
    temp += isRound(n, 366666)
    temp += isRound(n, 377777)
    temp += isRound(n, 388888)
    temp += isRound(n, 400000)
    temp += isRound(n, 411111)
    temp += isRound(n, 422222)
    temp += isRound(n, 433333)
    temp += isRound(n, 444444)
    temp += isRound(n, 455555)
    temp += isRound(n, 466666)
    temp += isRound(n, 477777)
    temp += isRound(n, 488888)
    temp += isRound(n, 500000)
    temp += isRound(n, 511111)
    temp += isRound(n, 522222)
    temp += isRound(n, 533333)
    temp += isRound(n, 543210)
    temp += isRound(n, 544444)
    temp += isRound(n, 555555)
    temp += isRound(n, 566666)
    temp += isRound(n, 577777)
    temp += isRound(n, 588888)
    temp += isRound(n, 600000)
    temp += isRound(n, 611111)
    temp += isRound(n, 622222)
    temp += isRound(n, 633333)
    temp += isRound(n, 644444)
    temp += isRound(n, 655555)
    temp += isRound(n, 666666)
    temp += isRound(n, 677777)
    temp += isRound(n, 688888)
    temp += isRound(n, 700000)
    temp += isRound(n, 711111)
    temp += isRound(n, 722222)
    temp += isRound(n, 733333)
    temp += isRound(n, 744444)
    temp += isRound(n, 755555)
    temp += isRound(n, 766666)
    temp += isRound(n, 777777)
    temp += isRound(n, 788888)
    temp += isRound(n, 800000)
    temp += isRound(n, 811111)
    temp += isRound(n, 822222)
    temp += isRound(n, 833333)
    temp += isRound(n, 844444)
    temp += isRound(n, 855555)
    temp += isRound(n, 866666)
    temp += isRound(n, 877777)
    temp += isRound(n, 888888)
    temp += isRound(n, 900000)
    temp += isRound(n, 911111)
    temp += isRound(n, 922222)
    temp += isRound(n, 933333)
    temp += isRound(n, 944444)
    temp += isRound(n, 955555)
    temp += isRound(n, 966666)
    temp += isRound(n, 977777)
    temp += isRound(n, 988888)
    temp += isRound(n, 1000000)
    temp += isRound(n, 1111111)
    temp += isRound(n, 1222222)
    temp += isRound(n, 1234567)
    temp += isRound(n, 1314520)

    if temp > 0:
        return True
    else:
        return False

def sendMail():
    try:
        dic = {}
        temp = {}
        for i in display_list:
            temp[i[1]] = {"item_id": int(i[0]), "剩余库存": i[2], "当前编号": i[3]}
        dic["收藏装扮"] = temp
        temp = {}
        for i in ending_list:
            temp[i[1]] = {"item_id": int(i[0]), "剩余库存": i[2], "当前编号": i[3]}
        dic["临近尾号"] = temp
        temp = {}
        # for i in good_list:
        #     temp[i[1]] = {"item_id": int(i[0]), "剩余库存": i[2], "当前编号": i[3]}
        # dic["临近靓号"] = temp
        # temp = {}
        # for i in return_list:
        #     temp[i[1]] = {"item_id": int(i[0]), "剩余库存": i[2], "当前编号": i[3]}
        # dic["全部装扮"] = temp
        # temp = {}
        mail_content = str(json.dumps(dic, sort_keys = False, indent = 4, separators=(',', ': '), ensure_ascii = False))

        if mail_on:
            mail_title = "自动全装扮监听"
            msg = MIMEMultipart()
            msg["Subject"] = Header(mail_title,'utf-8')
            msg["From"] = sender_qq
            # msg['To'] = ";".join(receiver)
            msg.attach(MIMEText(mail_content,'plain','utf-8'))
            smtp = SMTP_SSL(host_server)
            smtp.login(sender_qq,pwd)
            smtp.sendmail(sender_qq,receiver,msg.as_string())
            smtp.quit()
            print("邮件发送成功")

        for i in good_list:
            temp[i[1]] = {"item_id": int(i[0]), "剩余库存": i[2], "当前编号": i[3]}
        dic["临近靓号"] = temp
        temp = {}
        for i in return_list:
            temp[i[1]] = {"item_id": int(i[0]), "剩余库存": i[2], "当前编号": i[3]}
        dic["全部装扮"] = temp
        temp = {}
        
        if json_on:
            try:
                str_time = time.strftime("%Y_%m_%d_%H_%M_%S")
                with open(f"record_{str_time}.json","w") as f:
                    json.dump(dic, f, sort_keys = False, indent = 4, separators=(',', ': '), ensure_ascii = False)
                    print("文件写入完成")
            except:
                print("文件写入失败")
    except:
        print("邮件与json异常")

timer = 0
fav_timer = 0

while True:
    if time.time() - fav_timer > fav_listen_time:
        display_list = []
        print(time.asctime())
        fav_timer = time.time()
        for i in fav_list:
            try:
                reponse = requests.get(url.replace("Moon", str(i)), headers = headers)
                json_data = json.loads(reponse.text)
                item_name = json_data["data"]["name"]
                item_num = json_data["data"]["sale_surplus"]
                time.sleep(0.2)
                reponse = requests.get(url2.replace("Moon", str(i)), headers = headers)
                json_data = json.loads(reponse.text)
                now_num = json_data["data"]["rank"][0]["number"]
                t = (str(i), item_name, item_num, now_num)
                display_list.append(t)
                print(t)
                time.sleep(0.2)
            except:
                print(i)
                continue

    if time.time() - timer > all_listen_time:
        return_list = []
        ending_list = []
        good_list = []
        timer = time.time()
        for i in item_list:
            try:
                reponse = requests.get(url.replace("Moon", str(i)), headers = headers)
                json_data = json.loads(reponse.text)
                item_name = json_data["data"]["name"]
                item_num = json_data["data"]["sale_surplus"]
                time.sleep(0.2)
                reponse = requests.get(url2.replace("Moon", str(i)), headers = headers)
                json_data = json.loads(reponse.text)
                now_num = json_data["data"]["rank"][0]["number"]
                t = (str(i), item_name, item_num, now_num)
                return_list.append(t)
                print(t)
                if item_num < 1000 and i != 4755 and i != 1140:
                    ending_list.append(t)
                if isGoodNumber(int(now_num)):
                    good_list.append(t)
                time.sleep(0.2)
            except:
                print(i)
                continue
        sendMail()
