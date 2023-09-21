# Listen of Bilibili Designed by Moonkey_ 2022.08.10
# Copyright © 2022 Moonkey_, All Rights Reserved.
# pyinstaller -F -i icon.ico -w main.py

import os
import requests

api_header = {
    'user-agent':'Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 os/android model/Mi 10 build/6880300 osVer/11 sdkInt/30 network/2 BiliApp/6880300 mobi_app/android channel/xiaomi Buvid/XX185A1175A6B2CC78AC6AC2FDB57813F6EE1 sessionID/bca305d3 innerVer/6880310 c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 6.88.0 os/android model/Mi 10 mobi_app/android build/6880300 channel/xiaomi innerVer/6880310 osVer/11 network/2',
    'Referer': 'https://www.bilibili.com/',
    'sec-ch-ua':'Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104',
    'cookie': r'''buvid3=DD8E0EC3-967C-4EF3-4F5E-B558D04E58F590800infoc; i-wanna-go-back=-1; _uuid=B8B13A7A-484E-56210-9424-8D612EC7C610F90546infoc; buvid4=5623165E-DE74-A540-1E29-D808F1F3311F92240-022031500-pOTnPn1mSLHM7gp0IvFWYg==; buvid_fp_plain=undefined; buvid_fp=12ec06c99d3813205d1bd6fc4978b706; rpdid=|(J~JY|YuRY~0J'uYR~k~lkYY; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5516474282866283; nostalgia_conf=-1; blackside_state=0; hit-dyn-v2=1; is-2022-channel=1; b_nut=100; fingerprint3=eeda4c17fd99720ae6dec25b56a727a8; CURRENT_QUALITY=0; fingerprint=d220f8a49b0b8c31e303cd42735285b3; CURRENT_FNVAL=16; bp_video_offset_1060895791=undefined; DedeUserID=215177187; DedeUserID__ckMd5=db23a7f040ba3d37; b_ut=5; bp_video_offset_215177187=721715949438238700; SESSDATA=f1eb74d2,1682748098,f1a52*a2; bili_jct=887a075238db610a6c8929bb5ab2bb68; sid=66jyh2k9; innersign=0; b_lsid=1011044CDE_1843143CF67; PVID=1'''
}
id_url = "https://api.bilibili.com/x/garb/skin?id="

id = 38762
true = True
false = False
null = ""
while True:
    res = requests.get(url=id_url+str(id),headers=api_header)
    print(id)
    # print(id_url+str(id),res.text)
    if eval(res.text)["data"] != "":
        print(res.text)
        os.system("pause")
    id += 1
