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
from dataclasses import asdict

import pytest

from common.base_log import logger
from utils.allure_handle import AllureReportBeautiful
from utils.command_parser import command_parser
from common.mail_sender import MailSender
from common.robot_sender import EnterpriseWechatNotification
from common.settings import IS_SEND_EMAIL, IS_SEND_WECHAT, wechat_webhook_url, wechat_content, email_content, \
    email_config, max_fail, rerun, reruns_delay
from configs.paths_config import BASE_DIR, TEMP_DIR, PYTEST_REPORT_DIR, PYTEST_RESULT_DIR, ALLURE_REPORT_DIR, \
    FILES_DIR
from utils.data_handle import DataProcessor
from utils.file_handle import FileHandle
from utils.report_data_handle import ReportDataHandle

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
        f"--maxfail={max_fail}", f"--reruns={rerun}", f"--reruns-delay={reruns_delay}",  # 指定最大失败次数、重运行次数和重运行间隔时间
        '--alluredir', f'{TEMP_DIR}', '--clean-alluredir',  # 先清空旧的alluredir目录，再将生成Allure原始报告需要的数据,并存放在 /Temp 目录
        f'--html={os.path.join(PYTEST_REPORT_DIR, "pytest_report.html")}',  # 指定pytest-html报告的存放位置
        '--self-contained-html',  # 将css样式合并到pytest-html报告文件中，便于发送邮件
        '--json-report', '--json-report-summary',  # 生成简化版json报告
        f'--json-report-file={os.path.join(PYTEST_RESULT_DIR, "pytest_result.json")}',  # 指定json报告存放位置
        '--capture=no',  # 捕获stderr和stdout，这里是使pytest-html中失败的case展示错误日志，会导致case中的print不打印
        # '-p', 'no:logging',  # 表示禁用logging插件，使报告中不显示log信息，只会显示stderr和stdoyt信息,避免log和stderr重复。
        '-p', 'no:sugar',  # 禁用pytest-sugar美化控制台结果
        # '-k not test_login.py',  # 不执行该文件里的case
        # '-m smoke',  # 只运行mark标记为smoke的测试用例
        '-W', 'ignore:Module already imported so cannot be rewritten'
    ])

    # ------------------------------发送allure报告----------------------------------
    # 生成allure报告环境信息
    AllureReportBeautiful.set_report_env_on_results()
    # 生成allure报告执行器信息
    AllureReportBeautiful.set_report_executer_on_results()
    # 使用allure generate -o 命令将./Temp目录下的临时报告生成到Report目录下变成html报告
    os.system(f'allure generate {TEMP_DIR} -o {ALLURE_REPORT_DIR} --clean')
    # 修改allure报告浏览器窗口标题
    AllureReportBeautiful.set_windows_title("Sensoro自动化")
    # 修改allure报告标题
    AllureReportBeautiful.set_report_name("Sensoro自动化测试报告")
    # 将本地启动脚本和查看allure报告方法放入报告目录下面
    allure_files = os.path.join(FILES_DIR, 'allure_files')
    FileHandle.copy_file(allure_files + os.sep + 'open_report.sh', ALLURE_REPORT_DIR)
    FileHandle.copy_file(allure_files + os.sep + '查看allure报告方法', ALLURE_REPORT_DIR)

    # ------------------------------发送通知消息----------------------------------
    # 发送企业微信群聊
    pytest_result = asdict(ReportDataHandle.pytest_json_report_case_count())
    if IS_SEND_WECHAT:  # 判断是否需要发送企业微信
        EnterpriseWechatNotification(wechat_webhook_url).send_markdown(
            DataProcessor().process_data(wechat_content, pytest_result))

    # 发送邮件
    if IS_SEND_EMAIL:  # 判断是否需要发送邮件
        file_path = PYTEST_REPORT_DIR + os.sep + 'pytest_report.html'
        ms = MailSender(email_config)
        ms.attach_text(DataProcessor().process_data(email_content, pytest_result)).attach_file(file_path).send()
