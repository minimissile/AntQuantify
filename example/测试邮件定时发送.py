# import smtplib, ssl
# import schedule
# import time
#
# # 邮箱信息：
# sender_email = "minimissile01@163.com"  # 发送人邮箱，需为开启SMTP服务的邮箱
# receiver_email = "minimissile02@163.com"  # 接收人邮箱
# password = 'qq123456'  # 输入发送人邮箱密码
#
# message = """\
# Subject: Hi there!
#
# This message is sent from Python."""
#
#
# def send_email():
#     print('开始发送邮件')
#     port = 465  # For SSL
#     smtp_server = "smtp.gmail.com"
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
#         print("Email sent!")
#
#
# # 每天早上9点发送电子邮件
# # schedule.every().day.at("09:00").do(send_email)
# #
# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)
#
#
# if __name__ == "__main__":
#     send_email()
#
#
#
#
#
#
#


# import smtplib
# from email.mime.text import MIMEText
#
# # 邮件内容
# msg = MIMEText('邮件正文')
#
# # 发件人和收件人
# sender = 'minimissile01@163.com'
# recipient = 'minimissile02@163.com'
#
# # 设置邮件的头部信息
# msg['Subject'] = '邮件标题'
# msg['From'] = sender
# msg['To'] = recipient
#
# # 发送邮件
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# smtp_username = 'example@gmail.com'
# smtp_password = 'password'
#
# with smtplib.SMTP(smtp_server, smtp_port) as smtp:
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.login(smtp_username, smtp_password)
#     smtp.sendmail(sender, recipient, msg.as_string())


import zmail


mail_server = zmail.server(username='minimissile01@163.com', password='qq123456')
print('mail_server', mail_server)
mail = mail_server.get_latest()

print("邮件主题：", mail['Subject'])
print("邮件发送时间：", mail['Date'])
print("发送者：", mail['From'])
print("接收者：", mail['To'])
print("内容：\n", mail['content_text'])

# 获取指定id的邮件
mail = mail_server.get_mail(30)
zmail.show(mails=mail)

# 获取所有邮件
mails = mail_server.get_mails(start_time='2022-04-24', end_time='2022-04-25')
for mail in mails:
    print('-' * 20)
    zmail.show(mail)

# 发送邮件(带附件)
# file_path = 'D://temp/1.jpg'
mail_info = {
    'subject': '邮件主题',
    'content_text': '测试发送邮件',
    # 'attachments': file_path,
}

mail_server.send_mail('revice@qq.com', mail_info)
