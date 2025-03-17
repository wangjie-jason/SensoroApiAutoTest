#!/usr/bin/python
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
from common.base_log import logger
from common.exceptions import SendMessageError
from common.models import Email
from utils.MIME_type_classifier import get_MIME


class MailSender:
    """发送邮件功能"""

    def __init__(self, email_data: dict):
        email_data = Email(**email_data)
        self.subject = email_data.mail_subject  # 邮件标题
        self.sender_username = email_data.sender_username  # 发件人邮箱
        self.sender_password = email_data.sender_password  # 发件人邮箱授权码
        self.receiver_mail_list = email_data.receiver_mail_list  # 收件人邮箱
        self.smtp_domain = email_data.smtp_domain  # 发送邮箱的域名
        self.smtp_port = email_data.smtp_port  # 发送邮箱的端口号

        self.message = MIMEMultipart()
        self.message['From'] = Header(self.sender_username, 'utf-8')
        self.message['To'] = ';'.join(self.receiver_mail_list)
        self.message['subject'] = Header(self.subject, 'utf-8')

    def attach_text(self, content):
        """添加邮件正文内容"""
        self.message.attach(MIMEText(content, 'html', 'utf-8'))
        return self

    def attach_file(self, file_path):
        """添加附件"""
        with open(file_path, 'rb') as f:
            mime_app = MIMEApplication(f.read())
        mime_app['Content-Type'] = get_MIME(file_path)
        mime_app.add_header('content-disposition', 'attachment', filename='reporter.html')
        self.message.attach(mime_app)
        return self

    def send(self):
        logger.info("开始发送邮件")
        try:
            # 使用with可以加入超时等待30s，并且发送完成后自动关闭链接，省去了smtp_obj.quit()步骤
            with smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port, timeout=30) as smtp_obj:
                smtp_obj.login(self.sender_username, self.sender_password)
                smtp_obj.sendmail(from_addr=self.sender_username, to_addrs=self.receiver_mail_list,
                                  msg=self.message.as_string())
            logger.info("发送邮件成功")
        except smtplib.SMTPException as e:
            logger.error("Error: 无法发送邮件,失败原因:{}".format(e))
            raise SendMessageError(f'发送电子邮件时发生错误:{e}')
        except Exception as e:
            logger.error("Error: 无法发送邮件,失败原因:{}".format(e))
            raise


if __name__ == '__main__':
    email_config = {
        'mail_subject': '接口自动化测试报告',  # 邮件标题
        'sender_username': '1231323@qq.com',  # 发件人邮箱
        'sender_password': 'xxxxxxxxx',  # 发件人邮箱授权码
        'receiver_mail_list': ['1231323@qq.com', ],  # 收件人邮箱
        'smtp_domain': 'smtp.exmail.qq.com',  # 发送邮箱的域名
        'smtp_port': 465,  # 发送邮箱的端口号
    }
    MailSender(email_config).attach_text('测试邮件').attach_file(
        '/Users/wangjie/SensoroApiAutoTest/outFiles/pytest_report/pytest_report.html').send()
