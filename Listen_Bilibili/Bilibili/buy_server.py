# -*- coding:utf-8 -*-

from threading import Thread
import socket
import time
import json
import sys
import os
import requests

null = ""
true = True
false = False
flag = True
predict_time = 20 #ms 正提前, 负延后
addr = ("0.0.0.0", 23333)
# timer = time.time() * 1000 - predict_time

def getTime():
    try:
        res = requests.get(url="https://app.bilibili.com/x/v2/splash/show")
        return int(json.loads(res.text)["data"]["splash_request_id"][0:13])
    except Exception as e:
        print(e,"时间接口请求异常")
        os.system("pause")

def timerThread(timer: int):
    global flag
    session = requests.Session()

    try:
        while flag:
            res = session.get(url="https://app.bilibili.com/x/v2/splash/show")
            server_time = int(json.loads(res.text)["data"]["splash_request_id"][0:13])
            if server_time >= timer:
                flag = False
                break

    except Exception as e:
        print(e,"时间接口请求异常")
        os.system("pause")

    session.close()

def createThread(timer: int, num: int = 128):
    try:
        threads_list = []
        for i in range(num):
            t = Thread(target=timerThread, args=(timer,))
            threads_list.append(t)
        return threads_list
    except Exception as e:
        print(e, "创建线程异常")
        os.system("pause")

def startThread(t_list: list, num: int = 128):
    try:
        num = num if num <= len(t_list) else len(t_list)
        for i in range(num):
            t_list[i].start()
    except Exception as e:
        print(e, "启动线程异常")
        os.system("pause")

def joinThread(t_list: list, num: int = 128):
    try:
        num = num if num <= len(t_list) else len(t_list)
        for i in range(num):
            t_list[i].join()
    except Exception as e:
        print(e, "结束线程异常")
        os.system("pause")

def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(addr)
        server_socket.listen(1)
        print(f"服务端已开启...\n监听: {addr[0]}:{addr[1]}")
        global flag
    except Exception as e:
        print(e, "服务器启动异常")
        os.system("pause")

    while True:
        print("\n等待连接中...")
        try:
            client_connect, client_addr = server_socket.accept()
        except Exception as e:
            print(e, "客户端连接异常")
            # os.system("pause")
            continue

        flag = True
        print(client_addr," 已连接")
        print('等待接受时间信息...')
        try:
            sale_time = int(client_connect.recv(1024).decode("utf-8","ignore")) # 收消息
        except Exception as e:
            print(e, "客户端已关闭连接")
            client_connect.close()
            continue
        print(f"已接受到监听时间: {sale_time}")

        if getTime() >= sale_time:
            print("抢购已超时, 结束客户端连接")
            try:
                client_connect.send("-1".encode("utf-8", "ignore"))
            except Exception as e:
                print(e,"客户端已关闭连接")
            client_connect.close()
            continue
        else:
            bad_net = 0
            while True:
                if sale_time - getTime() > 10000:
                    try:
                        client_connect.send("1".encode("utf-8", "ignore"))
                        print("心跳验证在线...")
                        bad_net = 0
                        time.sleep(5)
                    except:
                        bad_net += 1
                        if bad_net >= 3:
                            print("客户端连接异常, 结束客户端连接")
                            client_connect.close()
                            break
                else:
                    t = time.time()
                    thread_list =  createThread(sale_time - predict_time, 128)
                    print("\n10s\n已创建时间请求线程")
                    print(time.time() - t)

                    while sale_time - getTime() > 5000:
                        time.sleep(0.5)

                    try:
                        client_connect.send("2".encode("utf-8", "ignore"))
                        print("\n已发送连接信号")
                    except Exception as e:
                        print(e)
                        print("\n信息发送异常, 已断开客户端连接")
                    t = time.time()
                    startThread(thread_list, 48)
                    print("\n5s\n已启动时间请求线程")
                    print(time.time() - t)

                    while True:
                        if not flag:
                            try:
                                client_connect.send("0".encode("utf-8", "ignore"))
                                print("\n已发送抢购信号, 结束客户端连接")
                            except Exception as e:
                                print(e)
                                print("\n信息发送异常, 已断开客户端连接")
                            break
                    client_connect.close()
                    joinThread(thread_list, 48)
                    print("\n已结束时间请求线程")
                    break

if __name__ == "__main__":
    main()
