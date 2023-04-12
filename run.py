#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import pytest

from common.mail_sender import MailSender
from common.settings import IS_SEND
from utils.get_yaml_data import get_yaml_data

if __name__ == '__main__':
    # 执行pytest单元测试，生成 Allure原始报告需要的数据存在 /Temp 目录
    pytest.main([
        '-vs',  # 指定输出用例执行信息，并打印程序中的print/logging输出
        'testCase/',  # 执行用例的目录
        '--alluredir', './Temp',  # 生成Allure原始报告需要的数据,并存放在 /Temp 目录
        '--html=./outFiles/pytest_report/report.html',  # 指定pytest-html报告的存放位置
        '--self-contained-html',  # 将css样式合并到pytest-html报告文件中，便于发送邮件
        # '--capture=sys',  # 仅捕获stderr，将stdout输出到终端，这里是使pytest-html中失败的case展示错误日志，会导致case中的prin不打印
        '-k not test_login.py',  # 不执行该文件里的case
    ])
    # 使用allure generate -o 命令将./Temp目录下的临时报告导出到TestReport目录
    os.system('allure generate ./Temp -o ./outFiles/report --clean')

    # 发送邮件
    if IS_SEND:
        file_path = '/Users/wangjie/SensoroApi/outFiles/pytest_report/report.html'
        with open(file_path, 'rb') as f:
            text_to_send = f.read()

        config = get_yaml_data('configs/mail_config.yaml')
        ms = MailSender(
            mail_subject=config['mail_subject'],
            sender_mail_address=config['sender_mail_address'],
            sender_username=config['sender_username'],
            sender_password=config['sender_password'],
            receiver_mail_list=config['receiver_mail_list'],
            smtp_domain=config['smtp_domain'],
            smtp_port=config['smtp_port'],
        )
        ms.attach_text(text_to_send).attach_file(file_path).send()
