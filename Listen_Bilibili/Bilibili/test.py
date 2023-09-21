import socket
import os
import time
import requests
import json

addr = ("127.0.0.1", 23333)
addr = ("Moonkey233.top", 23333)

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    print(f"{addr} 时间服务端连接成功")
    sale_time = str(int((time.time() + 15)*1000))
    s.send(sale_time.encode('utf-8')) # 发消息
    print(f"已发送购买时间: {sale_time}")

    while True:
        session = requests.session()
        session.get(url="https://app.bilibili.com/x/v2/splash/show")
        msg = int(s.recv(1024).decode("utf-8", "ingore"))
        if msg == -1:
            print(msg)
            break
        elif msg == 0:
            # print(msg)
            # print(time.time())
            res = session.get(url="https://app.bilibili.com/x/v2/splash/show")
            t = int(json.loads(res.text)["data"]["splash_request_id"][0:13])
            print(t)
            print(t - int(sale_time), "ms")
            break
        else:
            continue

    s.close()
    os.system("pause")