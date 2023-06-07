# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/5 11:48
# @Author : wangjie
# @File : robot_sender.py
# @project : SensoroApi

import os
import requests

from common.base_log import Logger
from common.exceptions import SendMessageError
from common.settings import ENV
from utils.report_data_handle import report_data_handle


def get_env_from_jenkins(name, base=''):
    """从Jenkins中获取全局环境变量"""
    return os.getenv(name) and os.getenv(name).strip() or base


ProjectName = get_env_from_jenkins("JOB_NAME")  # Jenkins构建项目名称
BUILD_URL = get_env_from_jenkins("BUILD_URL")  # Jenkins构建项目URL
BUILD_NUMBER = get_env_from_jenkins("BUILD_NUMBER")  # Jenkins构建编号
ALLURE_URL = BUILD_URL + 'allure/'


class EnterpriseWechatNotification:
    """企业微信群通知"""

    def __init__(self, hook_urls: list):
        # 企业微信群机器人的hook地址，一个机器人就一个，多个就定义多个，可以写死，也可以写在配置类中
        self.hook_urls = hook_urls
        self.header = {'Content-Type': 'application/json'}
        self.pytest_result = report_data_handle.pytest_json_report_case_count()

    def send_msg(self, msg='@all'):
        """发送企业微信消息通知"""
        logger = Logger().get_logger()

        content = f"""******用例执行结果统计******
        > 项目名称:{ProjectName}
        > 构件编号:#{BUILD_NUMBER}
        > 测试环境:{ENV.name}
        > 总用例数为：<font color=\"info\">{self.pytest_result['total_case']}条</font>
        > 通过用例数为：<font color=\"info\">{self.pytest_result['pass_case']}条</font>
        > 失败用例数为：<font color=\"error\">{self.pytest_result['fail_case']}条</font>
        > 跳过用例数为：<font color=\"comment\">{self.pytest_result['skip_case']}条</font>
        > 预期失败用例数为：<font color=\"warning\">{self.pytest_result['xfail_case']}条</font>
        > 预期通过用例数为：<font color=\"comment\">{self.pytest_result['xpass_case']}条</font>
        > 报错用例数为：<font color=\"error\">{self.pytest_result['error_case']}条</font>
        > 通过率为：<font color=\"info\">{self.pytest_result['pass_rate']}%</font>
        > 用例执行时间为：<font color=\"info\">{self.pytest_result['case_duration']}s</font>
        > 测试报告，点击查看>>[测试报告入口]({ALLURE_URL})
        > 构建详情，点击查看>>[控制台入口]({BUILD_URL})
        {msg}"""

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
                "mentioned_list": ["汪杰", "@all"],
                "mentioned_mobile_list": ['13718395478', "@all"]

            },
        }

        for hook_url in self.hook_urls:
            response = requests.post(url=hook_url, headers=self.header, json=payload)
            result = response.json()
            if result["errcode"] == 0:
                logger.info("企业微信消息发送成功")
            else:
                logger.error(f'企业微信「MarkDown类型」消息发送失败：{response.json()}')
                raise SendMessageError(f"企业微信「MarkDown类型」消息发送失败，错误代码：{result['errcode']}，错误信息：{result['errmsg']}")


if __name__ == '__main__':
    EnterpriseWechatNotification(
        ['https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50ab5cc5-7b5d-4ed0-a95b-ddd5daeeec5c']).send_msg()
