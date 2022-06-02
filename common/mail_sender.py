# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/1 16:20
# @Author : wangjie
# @File : mail_sender.py
# @project : SensoroApi
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.base_log import Logger


class MailSender:
    """发送邮件功能"""

    def __init__(self, mail_subject, sender_mail_address, sender_username, sender_password, receiver_mail_list,
                 smtp_domain, smtp_port):
        self.subject = mail_subject
        self.sender_mail_address = sender_mail_address
        self.sender_username = sender_username
        self.sender_password = sender_password
        self.receiver_mail_list = receiver_mail_list
        self.smtp_domain = smtp_domain
        self.smtp_port = smtp_port

        self.message = MIMEMultipart()
        self.message['From'] = Header(self.sender_mail_address, 'utf-8')
        self.message['To'] = ';'.join(self.receiver_mail_list)
        self.message['subject'] = Header(self.subject, 'utf-8')

    def attach_text(self, text_to_send):
        """添加邮件正文内容"""
        self.message.attach(MIMEText(text_to_send, 'html', 'utf-8'))
        return self

    def attach_file(self, file_path):
        """添加附件"""
        mime_app = MIMEApplication(open(file_path, 'r').read())
        mime_app['Content-Type'] = 'application/octet-stream'
        # mime_app['Content-Type'] = 'text/html'
        mime_app.add_header('content-disposition', 'attachment', filename='reporter.html')
        self.message.attach(mime_app)
        return self

    def send(self):
        logger = Logger().get_logger()
        logger.info("开始发送邮件")
        try:
            smtp_obj = smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port)
            smtp_obj.login(self.sender_username, self.sender_password)
            smtp_obj.sendmail(from_addr=self.sender_mail_address, to_addrs=self.receiver_mail_list,
                              msg=self.message.as_string())
            smtp_obj.quit()
            logger.info("发送邮件成功")
        except smtplib.SMTPException as e:
            logger.error("Error: 无法发送邮件,失败原因:{}".format(e))
        except Exception as e:
            logger.error("Error: 无法发送邮件,失败原因:{}".format(e))


if __name__ == '__main__':
    mail_send = MailSender('测试邮件发送', 'wangjie@sensoro.com', 'wangjie@sensoro.com', 'PeeuobDpukzEcD54',
                           ['wangjie@sensoro.com'], 'smtp.exmail.qq.com', 465).attach_text(
        '测试邮件').attach_file('/Users/wangjie/SensoroApi/outFiles/report').send()
