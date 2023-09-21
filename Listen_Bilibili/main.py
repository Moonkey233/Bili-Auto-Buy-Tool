# ©Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright © 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

import os
import sys
import time
import json
import pygame as pg
import urllib.parse
import urllib.request
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

num_buy = 10 #设置购买秒杀套数1-10
uid_bili = 392774666 #设置购买用户UID, 目前就显示用
total = 30000 #设置装扮库存总数
expectation = 22222 #设置预期抢购的编号
fresh_sec = 0.1 #设置刷新的间隔
fresh_sec2 = 0.1 #设置100套内刷新的间隔
item_id = 37825 #设置监听装扮id, 断网或抓包获得网址后网页调试获得
sound_on = False #设置购买更新提示音
mail_on = False #设置邮件提示开启
deviation_predict = 0 #设置预判偏移量, 0或一个正整数, 慎用
mail_num = 500 #设置邮件提前提醒数量
receiver = ['3422180797@qq.com', 'Moonkey233@foxmail.com'] #设置通知接受邮箱地址
cmd = r''''''
'''抓包设置curl自动post地址'''

#初始化pygame, 载入资源
pg.init()
try:
    icon = pg.image.load('res/icon.ico')
    pg.display.set_icon(icon)
except:
    print("图片资源载入失败, 请检查")
try:
    font = pg.font.Font('res/font.ttf', 30)
    font2 = pg.font.Font('res/font.ttf', 20)
    font3 = pg.font.Font('res/font.ttf', 15)
except:
    font = pg.font.SysFont('微软雅黑', 30)
    font2 = pg.font.SysFont('微软雅黑', 20)
    font3 = pg.font.SysFont('微软雅黑', 15)
    print("字体资源载入失败, 请检查")
try:
    sound_info = pg.mixer.Sound("res/info.mp3")
except:
    sound_on = False
    print("音频资源载入失败, 请检查")

#初始化变量参数
dic = {}
dic2 = {}
null = ""
item_name = ""
lastest_name = ""
flag = 0
count = 0
mail_type = 0
num = "0"
number = 0
lastest_id = "0"
timer = 0
bad_net = 0
true_number = 0
init_time = time.time()
lastest_time = time.time()
size = width, height = 360, 500
host_server = 'smtp.qq.com'
sender_qq = 'Moonkey_Work@foxmail.com'
pwd = 'nsjwkzmtikncbibf'
mail_title = item_name + " 监听预期临近通知"
url = 'https://api.bilibili.com/x/garb/v2/mall/suit/detail?csrf=495347a5e1ff372a0b7c558af50bfa87&from=&from_id=&item_id='+ str(item_id) +'&part=suit'
url2 = 'https://api.bilibili.com/x/garb/rank/fan/recent?csrf=495347a5e1ff372a0b7c558af50bfa87&item_id=' + str(item_id)
header = {
    'user-agent':'Mozilla/5.0 (Linux; Android 12; Mi 10 Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.78 Mobile Safari/537.36 os/android model/Mi 10 build/6840300 osVer/12 sdkInt/31 network/2 BiliApp/6840300 mobi_app/android channel/xiaomi Buvid/XX185A1175A6B2CC78AC6AC2FDB57813F6EE1 sessionID/80031f98 innerVer/6840310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.84.0 os/android model/Mi 10 mobi_app/android build/6840300 channel/xiaomi innerVer/6840310 osVer/12 network/2',
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': r'''buvid3=DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc; i-wanna-go-back=-1; _uuid=B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc; buvid4=5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==; buvid_fp_plain=undefined; buvid_fp=12ec06c99d3813205d1bd6fc4978b706; rpdid=|(J~JY|YuRY~0J'uYR~k~lkYY; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5516474282866283; nostalgia_conf=-1; blackside_state=0; hit-dyn-v2=1; CURRENT_QUALITY=120; bp_video_offset_416166928=697567164921544800; innersign=0; b_lsid=519887E7_182CED8C228; CURRENT_FNVAL=16; bp_video_offset_215177187=697895274748575900; sid=83dmlo5x; fingerprint3=3f1b7a30861b19380f9fd5561f012e65; fingerprint=11c1eb1bdc041bada2eb9a575b2f9080; DedeUserID=392774666; DedeUserID__ckMd5=b0a7c64e70aeca8e; SESSDATA=a7e0f0e7,1676883295,de05f*81; bili_jct=4dbfc8a9f511b286b87fa1571a12669f; b_ut=5; PVID=3; b_timer={"ffp":{"333.1007.fp.risk_DD8E0EC3":"182CF0FDD16","333.42.fp.risk_DD8E0EC3":"182CED8CBE2","333.1193.fp.risk_DD8E0EC3":"182CED911C5","333.859.fp.risk_DD8E0EC3":"182CF12465D","333.885.fp.risk_DD8E0EC3":"182CEE04663","333.979.fp.risk_DD8E0EC3":"182CEE0498A"}}'''
}

#设置pygame窗口属性
screen = pg.display.set_mode(size)
if sound_on:
    pg.mixer.Sound.set_volume(sound_info, 1)
pg.display.set_caption("B站粉丝装扮监听 Moonkey_ 2022")

if __name__ == "__main__":
    '''主函数'''
    while True:
        screen.fill((0, 0, 0)) #填充黑色
        for event in pg.event.get(): #事件防止死循环
            if event.type == pg.QUIT:
                sys.exit()

        #刷新请求申请
        if time.time() - timer > fresh_sec:
            try:
                #爬虫请求
                if timer == 0:
                    req = urllib.request.Request(url, method = 'GET', headers = header)
                    reponse = urllib.request.urlopen(req)
                    data = str(reponse.read(), encoding = "utf-8")
                    dic = json.loads(data)
                    item_name = dic["data"]["name"]
                    num = str(dic["data"]["sale_surplus"])
                req2 = urllib.request.Request(url2, method = 'GET', headers = header)
                reponse2 = urllib.request.urlopen(req2)

                #获取文本, 解码
                data2 = str(reponse2.read(), encoding = "utf-8")

                #转json dict解析获取当前库存、最新rank
                dic2 = json.loads(data2)
                number = dic2["data"]["rank"][0]["number"]

                true_number = int(number) if int(number) >= int(lastest_id) else int(lastest_id)

                #post发包curl请求购买
                if true_number + num_buy >= expectation and true_number + 1 <= expectation:
                    os.system(cmd)

                bad_net = 0

            except:
                bad_net += 1

            #发生新的购买记录
            if int(lastest_id) < int(number):

                lastest_name = dic2["data"]["rank"][0]["nickname"]
                lastest_time = time.time() #记录时间与id
                lastest_id = number

                if sound_on:
                    try:
                        sound_info.play() #提示音
                    except:
                        pass

                #加快刷新频率
                if expectation - true_number - 1 <= 100 and fresh_sec > fresh_sec2:
                        fresh_sec = fresh_sec2
                #邮件通知
                if mail_type == 0 and expectation - true_number - 1 <= mail_num and expectation - true_number - 1 > mail_num - 10:
                    mail_type = 1

                    #邮件配置与发送
                    if mail_on:
                        try:
                            mail_content = "您监听的B站装扮 " + item_name + " 第(" + str(true_number) + ")套已被购买, 距预期(" + str(expectation) + ")仅间隔 【" + str(expectation - int(true_number) - 1) + "】 套, 请留意购买。"
                            msg = MIMEMultipart()
                            msg["Subject"] = Header(mail_title,'utf-8')
                            msg["From"] = sender_qq
                            msg['To'] = ";".join(receiver)
                            msg.attach(MIMEText(mail_content,'plain','utf-8'))
                            smtp = SMTP_SSL(host_server)
                            smtp.login(sender_qq,pwd)
                            smtp.sendmail(sender_qq,receiver,msg.as_string())
                            smtp.quit()
                        except:
                            print("邮件发送异常")

            #更新计时器
            timer = time.time()

        #判定是否为可购买范围
        if true_number + num_buy >= expectation and true_number + 1 <= expectation:
            flag = 1
        elif true_number + 1 > expectation:
            #邮件配置与发送
            if mail_on and flag != 2:
                try:
                    mail_content = "您监听的B站装扮 " + item_name + " 预期【" + str(expectation) + "】抢购结束, 请前往B站客户端检查是否抢购成功。"
                    msg = MIMEMultipart()
                    msg["Subject"] = Header(mail_title,'utf-8')
                    msg["From"] = sender_qq
                    msg['To'] = ";".join(receiver)
                    msg.attach(MIMEText(mail_content,'plain','utf-8'))
                    smtp = SMTP_SSL(host_server)
                    smtp.login(sender_qq,pwd)
                    smtp.sendmail(sender_qq,receiver,msg.as_string())
                    smtp.quit()
                except:
                    print("邮件发送异常")
            flag = 2

        if bad_net >= 1 and bad_net <= 5:
            text = font3.render("网络异常, 重试中...第" + str(bad_net) + "/5次", True, (255, 0, 0))
            screen.blit(text, (0, 10))

        if bad_net > 5:
            text = font3.render("网络异常请重启,若无法解决,请15分钟后尝试或更换IP", True, (255, 0, 0))
            screen.blit(text, (0, 10))
            try:
                sound_info.play() #提示音
            except:
                pass

        #界面显示
        text = font2.render(item_name + " 实时监听: ", True, (0, 255, 0))
        screen.blit(text, (0, 30))

        text = font2.render("用户UID: " + str(uid_bili) + " 欲购买套数: " + str(num_buy), True, (0, 255, 0))
        screen.blit(text, (0, 60))

        text = font2.render("库存: " + num + "(节约性能, 暂停更新)", True, (255, 255, 255))
        screen.blit(text, (0, 100))

        text = font2.render("参考: " + str(total + 1 - int(num)) + "(没什么用, 看实际购买范围)", True, (255, 255, 255))
        screen.blit(text, (0, 150))

        text = font2.render("最新: " + str(lastest_id) + " ID: " + lastest_name, True, (0, 191, 255))
        screen.blit(text, (0, 200))

        text = font2.render("剩余开抢间隔: 【" + str(expectation - true_number - num_buy) + "】 套", True, (0, 191, 255))
        screen.blit(text, (0, 220))

        text = font.render("实际: " + str(true_number + 1) + " ~ " + str(true_number + num_buy), True, (255 if flag != 1 else 0, 255 if flag != 2 else 0, 0))
        screen.blit(text, (15, 250))

        text = font3.render("(下次可购买范围,绿色可购买,红色已被购买,黄色等待)", True, (255, 255, 255))
        screen.blit(text, (5, 300))

        text = font.render(str(int(time.time() - float(lastest_time))) + "秒前有更新", True, (0, 255, 0))
        screen.blit(text, (90, 330))

        text = font2.render(str(time.asctime()), True, (255, 192, 203))
        screen.blit(text, (60, 370))

        text = font3.render("程序已运行" + str(int(time.time() - init_time)) + "秒", True, (255, 192, 203))
        screen.blit(text, (120, 400))

        text = font3.render("期望: " + str(expectation) + " 总库存: " + str(total) + " 刷新间隔: " + str(fresh_sec) + "秒", True, (255, 0, 0))
        screen.blit(text, (25, 430))

        text = font3.render("距期望" + str(mail_num) + "套时, 将进行邮件通知并加速刷新频率", True, (255, 255, 255))
        screen.blit(text, (20, 450))

        text = font3.render("装扮靓号代抢,开发者QQ2472272041,B站-Moonkey-", True, (0, 0, 255))
        screen.blit(text, (0, 480))

        #刷新显示
        pg.display.update()
