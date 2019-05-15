# coding: utf8
import base64
from user_properties import RECEIVER_ADDRESS, SENDER_ADDRESS, EMAIL_PASSWORD
import smtplib
from email.mime.text import MIMEText


class Email:
    @staticmethod
    def send(title, content):
        server = smtplib.SMTP('smtp.126.com')
        server.login(SENDER_ADDRESS, str(base64.b64decode(EMAIL_PASSWORD), 'utf8'))
        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = SENDER_ADDRESS
        message['To'] = RECEIVER_ADDRESS
        message['Subject'] = title
        server.sendmail(
            SENDER_ADDRESS,
            RECEIVER_ADDRESS,
            message.as_string())
        server.quit()


