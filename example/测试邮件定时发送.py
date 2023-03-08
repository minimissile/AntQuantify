# ---------------------------------------下面发送邮件的方式需要邮箱已登录------------------------------------------
import smtplib
import ssl
import config.jq as jq

email = jq.Email()


def send_email(receiver_email, message):
    """
    发送邮件
    :param receiver_email: 收件邮箱
    :param message: 要发送的信息
    :return:
    """

    print('开始发送邮件')
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(email.smtp_server, email.port, context=context) as server:
        server.login(email.sender_email, email.password)
        server.sendmail(email.sender_email, receiver_email, message)
        print("邮件发送成功")
        return True


if __name__ == "__main__":
    test_receiver_email = "minimissile01@163.com"  # 接收人邮箱
    test_message = """\
    Subject: Hi there!

    {}""".format('你好!')
    send_email(test_receiver_email, test_message)
    print(email.sender_email)
