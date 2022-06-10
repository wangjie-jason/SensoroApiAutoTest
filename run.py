#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import pytest

from common.mail_sender import MailSender
from tools.get_yaml_data import get_yaml_data

if __name__ == '__main__':
    # # 执行pytest单元测试，生成 Allure原始报告需要的数据存在 /Temp 目录
    # pytest.main(['-vs', 'testCase/', '--alluredir', './Temp'])
    # # 使用allure generate -o 命令将./Temp目录下的临时报告导出到TestReport目录
    # os.system('allure generate ./Temp -o ./outFiles/report --clean')

    pytest.main()
    os.system('allure generate ./Temp -o ./outFiles/report --clean')

    # 发送邮件
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
