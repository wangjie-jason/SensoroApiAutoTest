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
from common.base_log import logger


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

    def get_MIME(self, file_name):
        """多用途互联网邮件扩展类型，根据发送文件的后缀匹配对应的类型"""
        d = {
            'image/png': ['png'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['xlsx'],
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['pptx'],
            'application/pdf': ['pdf'],
            'image/jpeg': ['jpg', 'jpeg'],
            'application/zip': ['zip'],
            'text/plain': ['txt'],
            'video/mp4': ['mp4'],
            'application/msword': ['doc', 'dot'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.template': ['dotx'],
            'application/vnd.ms-word.document.macroEnabled.12': ['docm'],
            'application/vnd.ms-word.template.macroEnabled.12': ['dotm'],
            'application/vnd.ms-excel': ['xls', 'xlt', 'xla'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.template': ['xltx'],
            'application/vnd.ms-excel.sheet.macroEnabled.12': ['xlsm'],
            'application/vnd.ms-excel.template.macroEnabled.12': ['xltm'],
            'application/vnd.ms-excel.addin.macroEnabled.12': ['xlam'],
            'application/vnd.ms-excel.sheet.binary.macroEnabled.12': ['xlsb'],
            'application/vnd.ms-powerpoint': ['ppt', 'pot', 'pps', 'ppa'],
            'application/vnd.openxmlformats-officedocument.presentationml.slideshow': ['ppsx'],
            'application/vnd.ms-powerpoint.addin.macroEnabled.12': ['ppam'],
            'application/vnd.ms-powerpoint.presentation.macroEnabled.12': ['pptm', 'potm'],
            'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': ['ppsm'],
            'application/x-tar': ['tar'],
        }
        # 获取文件后缀
        hz = file_name.split('.')[-1]
        for key, value in d.items():
            if hz in value:
                return key
        return 'application/octet-stream'  # 一切未知类型

    def attach_text(self, text_to_send):
        """添加邮件正文内容"""
        self.message.attach(MIMEText(text_to_send, 'html', 'utf-8'))
        return self

    def attach_file(self, file_path):
        """添加附件"""
        with open(file_path, 'rb') as f:
            mime_app = MIMEApplication(f.read())
        mime_app['Content-Type'] = self.get_MIME(file_path)
        mime_app.add_header('content-disposition', 'attachment', filename='reporter.html')
        self.message.attach(mime_app)
        return self

    def send(self):
        logger.info("开始发送邮件")
        try:
            # 使用with可以加入超时等待30s，并且发送完成后自动关闭链接，省去了smtp_obj.quit()步骤
            with smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port, timeout=30) as smtp_obj:
                smtp_obj.login(self.sender_username, self.sender_password)
                smtp_obj.sendmail(from_addr=self.sender_mail_address, to_addrs=self.receiver_mail_list,
                                  msg=self.message.as_string())
            logger.info("发送邮件成功")
        except smtplib.SMTPException as e:
            logger.error("Error: 无法发送邮件,失败原因:{}".format(e))
        except Exception as e:
            logger.error("Error: 无法发送邮件,失败原因:{}".format(e))


if __name__ == '__main__':
    MailSender('测试邮件发送', 'wangjie@sensoro.com', 'wangjie@sensoro.com', 'PeeuobDpukzEcD54',
               ['wangjie@sensoro.com'], 'smtp.exmail.qq.com', 465).attach_text(
        '测试邮件').attach_file('/Users/wangjie/SensoroApi/outFiles/pytest_report/report.html').send()
