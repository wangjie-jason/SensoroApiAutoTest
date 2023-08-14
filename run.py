#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
运行方式说明：
  > python3 run.py  (默认在test环境运行测试用例)
  > python3 run.py -env DEV/TEST/PROD/DIANJUN 在对应环境运行测试用例
  > python3 run.py --send-wechat True/False 指定是否需要发送企业微信群消息
  > python3 run.py --send-email True/False 指定是否需要发送邮件
"""

import os
import shutil

import pytest

from common.base_log import logger
from utils.command_parser import command_parser
from common.mail_sender import MailSender
from common.robot_sender import EnterpriseWechatNotification
from common.settings import IS_SEND_EMAIL, IS_SEND_WECHAT
from configs.dir_path_config import BASE_DIR, TEMP_DIR, ALLURE_REPORT_DIR, PYTEST_REPORT_DIR, CONFIGS_DIR, \
    PYTEST_RESULT_DIR
from utils.yaml_handle import YamlHandle

if __name__ == '__main__':
    logger.info("""
                             _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | "_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  Starting      ...     ...     ...
                """)

    # 获取命令行参数中指定的通知状态，如果没有的话就用settings中指定的通知状态
    args = command_parser()
    IS_SEND_EMAIL = eval(args.send_email) if args.send_email else IS_SEND_EMAIL
    IS_SEND_WECHAT = eval(args.send_wechat) if args.send_wechat else IS_SEND_WECHAT

    pytest.main([
        # '-q',  # 代表 "quiet"，即安静模式，它可以将 pytest 的输出精简化，只输出测试用例的执行结果，而不会输出额外的信息，如测试用例的名称、执行时间等等
        '-vs',  # 指定输出用例执行信息，并打印程序中的print/logging输出
        'testCase/',  # 执行用例的目录
        '--alluredir', f'{TEMP_DIR}', '--clean-alluredir',  # 先清空旧的alluredir目录，再将生成Allure原始报告需要的数据,并存放在 /Temp 目录
        f'--html={os.path.join(PYTEST_REPORT_DIR, "pytest_report.html")}',  # 指定pytest-html报告的存放位置
        '--json-report', '--json-report-summary',  # 生成简化版json报告
        f'--json-report-file={os.path.join(PYTEST_RESULT_DIR, "pytest_result.json")}',  # 指定json报告存放位置
        '--self-contained-html',  # 将css样式合并到pytest-html报告文件中，便于发送邮件
        '--capture=no',  # 捕获stderr和stdout，这里是使pytest-html中失败的case展示错误日志，会导致case中的print不打印
        # '-p', 'no:logging',  # 表示禁用logging插件，使报告中不显示log信息，只会显示stderr和stdoyt信息,避免log和stderr重复。
        '-p', 'no:sugar',  # 禁用pytest-sugar美化控制台结果
        # '-k not test_login.py',  # 不执行该文件里的case
        # '-m smoke',  # 只运行mark标记为smoke的测试用例
    ])

    ###################发送allure报告
    # allure报告展示environment时所需要的数据，这里是在项目根路径下创建的environment.properties文件拷贝到allure-report报告中,保证环境文件不会被清空
    shutil.copy(BASE_DIR + os.sep + 'environment.properties', TEMP_DIR + os.sep + 'environment.properties')
    # allure报告展示运行器时所需要的数据
    shutil.copy(BASE_DIR + os.sep + 'executor.json', TEMP_DIR + os.sep + 'executor.json')
    # 使用allure generate -o 命令将./Temp目录下的临时报告生成到Report目录下变成html报告
    os.system(f'allure generate {TEMP_DIR} -o {ALLURE_REPORT_DIR} --clean')
    # 将本地启动脚本和查看allure报告方法放入报告目录下面
    shutil.copy(BASE_DIR + os.sep + 'open_report.sh', ALLURE_REPORT_DIR + os.sep + 'open_report.sh')
    shutil.copy(BASE_DIR + os.sep + '查看allure报告方法', ALLURE_REPORT_DIR + os.sep + '查看allure报告方法')

    # 发送企业微信群聊
    if IS_SEND_WECHAT:  # 判断是否需要发送企业微信
        EnterpriseWechatNotification(
            [
                'hook_url']).send_markdown(
            "<@汪杰>")

    # 发送邮件
    if IS_SEND_EMAIL:  # 判断是否需要发送邮件
        file_path = PYTEST_REPORT_DIR + os.sep + 'pytest_report.html'
        with open(file_path, 'rb') as f:
            text_to_send = f.read()

        config = YamlHandle(CONFIGS_DIR + os.sep + 'mail_config.yaml').read_yaml()
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
