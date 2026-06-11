#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
运行方式说明：
  > python3 run.py  (默认在test环境运行测试用例)
  > python3 run.py -env DEV/TEST/PROD/DIANJUN/WUFENG 在对应环境运行测试用例
  > python3 run.py --send-wechat True/False 指定是否需要发送企业微信群消息
  > python3 run.py --send-email True/False 指定是否需要发送邮件
"""

import os
from dataclasses import asdict

import pytest

from core.config_manager import config
from core.logger import logger
from core.paths import ALLURE_RESULT, PYTEST_REPORT_DIR, PYTEST_RESULT_DIR, ALLURE_REPORT_DIR
from utils.allure_util import AllureReportBeautiful
from utils.data_util import DataProcessor
from utils.mail_sender import MailSender
from utils.report_data_handle import ReportDataHandle
from utils.robot_sender import EnterpriseWechatNotification

if __name__ == '__main__':
    logger.info(f"""
                             _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | "_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  Starting      ...     ...     ...
                  Environment: {config.current_env()}
                  Base URL: {config.base_url()}
                """)

    pytest.main([
        # '-q',  # 代表 "quiet"，即安静模式，它可以将 pytest 的输出精简化，只输出测试用例的执行结果，而不会输出额外的信息，如测试用例的名称、执行时间等等
        '-vs',  # 指定输出用例执行信息，并打印程序中的print/logging输出
        'testcase/',  # 执行用例的目录
        f"--maxfail={config.max_fail_count()}",  # 指定最大失败次数
        f"--reruns={config.rerun_count()}", f"--reruns-delay={config.rerun_delay_seconds()}",  # 指定重运行次数和重运行间隔时间
        '--alluredir', f'{ALLURE_RESULT}', '--clean-alluredir',
        # 先清空旧的alluredir目录，再将生成Allure原始报告需要的数据,并存放在 /allure_result 目录
        f'--html={PYTEST_REPORT_DIR / "pytest_report.html"}',  # 指定pytest-html报告的存放位置
        '--self-contained-html',  # 将css样式合并到pytest-html报告文件中，便于发送邮件
        '--json-report', '--json-report-summary',  # 生成简化版json报告
        f'--json-report-file={PYTEST_RESULT_DIR / "pytest_result.json"}',  # 指定json报告存放位置
        '--capture=no',  # 捕获stderr和stdout，这里是使pytest-html中失败的case展示错误日志，会导致case中的print不打印
        # '-p', 'no:logging',  # 表示禁用logging插件，使报告中不显示log信息，只会显示stderr和stdoyt信息,避免log和stderr重复。
        '-p', 'no:sugar',  # 禁用pytest-sugar美化控制台结果
        # '-k not test_login.py',  # 不执行该文件里的case
        # '-m smoke',  # 只运行mark标记为smoke的测试用例
        '-W', 'ignore:Module already imported so cannot be rewritten'  # 忽略faker库在pytest自动导入后无法被重写警告
    ])

    # ------------------------------发送allure报告----------------------------------
    try:
        # 生成allure报告环境信息
        AllureReportBeautiful.set_report_env_on_results()
        # 生成allure报告执行器信息
        AllureReportBeautiful.set_report_executer_on_results()
        # 使用allure generate -o 命令将./Temp目录下的临时报告生成到Report目录下变成html报告
        ret = os.system(f'allure generate {ALLURE_RESULT} -o {ALLURE_REPORT_DIR} --clean')
        if ret != 0:
            raise RuntimeError("allure generate 失败, 可能缺少 Java 或 allure CLI")
        # 修改allure报告浏览器窗口标题
        AllureReportBeautiful.set_windows_title(config.project_name())
        # 修改allure报告标题
        AllureReportBeautiful.set_report_name(config.project_name())
    except Exception:
        logger.warning("Allure 报告生成失败, 跳过报告美化, 原始数据仍可用", exc_info=True)

    # ------------------------------发送通知消息----------------------------------
    # 获取pytest-json报告数据
    pytest_result = asdict(ReportDataHandle.pytest_json_report_case_count())

    # 发送企业微信群聊
    if config.is_send_wechat():  # 判断是否需要发送企业微信
        EnterpriseWechatNotification(config.wechat_webhook_urls()).send_markdown(
            DataProcessor().process_data(config.wechat_content(), pytest_result))

    # 发送邮件
    if config.is_send_email():  # 判断是否需要发送邮件
        file_path = PYTEST_REPORT_DIR / 'pytest_report.html'
        ms = MailSender(config.email_config())
        ms.attach_text(DataProcessor().process_data(config.email_content(), pytest_result)).attach_file(
            file_path).send()
