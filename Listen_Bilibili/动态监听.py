from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import requests
import winsound
import json
import time
import os

# uid = input("uid: ")
uid = 1210018134
receiver = ['Moonkey233@foxmail.com']
host_server = 'smtp.qq.com'
sender_qq = 'Moonkey_Work@foxmail.com'
pwd = 'cgqkfvjxmmctbhjj'

def send_mail(title, mail_content):
    try:
        mail_title = title
        msg = MIMEMultipart()
        msg["Subject"] = Header(mail_title,'utf-8')
        msg["From"] = sender_qq
        msg['To'] = ";".join(receiver)
        msg.attach(MIMEText(mail_content,'plain','utf-8'))
        smtp = SMTP_SSL(host_server)
        smtp.login(sender_qq,pwd)
        smtp.sendmail(sender_qq,receiver,msg.as_string())
        smtp.quit()
        # print(title + " 邮件发送成功")
    except:
        print("邮件发送异常")

def main():
    dynid = 0
    while True:
        try:
            req = requests.get(url=f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}&offset_dynamic_id=0")
            data = json.loads(req.text)
            tid = int(data['data']['cards'][0]['desc']['dynamic_id'])
            print(f'\r{int(time.time())} {tid}', end='')
            if tid != dynid:
                if dynid != 0:
                    print("\nUP动态有更新\n")
                    winsound.Beep(500, 1000)
                    send_mail("UP动态监听通知", f"UP(uid: {uid})发动态啦!")
                dynid = tid
            time.sleep(1)
        except Exception as e:
            print(e)
            os.system("pause")
            pass

if __name__ == '__main__':
    # send_mail("UP动态监听通知", f"UP(uid: {uid})发动态啦!")
    print(time.time())
    main()
