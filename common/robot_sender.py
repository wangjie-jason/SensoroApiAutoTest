# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/5 11:48
# @Author : wangjie
# @File : robot_sender.py
# @project : SensoroApi

import os
import json
import requests
import platform

from common.settings import ENV
from utils.get_local_ip import get_host_ip
from utils.report_data_handle import report_data_handle


def get_env_from_jenkins(name, base=''):
    """从Jenkins中获取全局环境变量"""
    return os.getenv(name) and os.getenv(name).strip() or base


ProjectName = get_env_from_jenkins("JOB_NAME")  # Jenkins构建项目名称
BUILD_URL = get_env_from_jenkins("BUILD_URL")  # Jenkins构建项目URL
BUILD_NUMBER = get_env_from_jenkins("BUILD_NUMBER")  # Jenkins构建编号


class EnterpriseWechatNotification:
    """企业微信群通知"""

    def __init__(self, hook_urls: list):
        # 企业微信群机器人的hook地址，一个机器人就一个，多个就定义多个，可以写死，也可以写在配置类中
        self.hook_urls = hook_urls
        # allure生成报告的地址，Jenkins执行时会用到，Windows暂未配置allure地址
        self.allure_url = f"http://{get_host_ip()}:8080/jenkins/job/{ProjectName}/{BUILD_NUMBER}/allure/"
        self.header = {'Content-Type': 'application/json'}
        self.pytest_result = report_data_handle.pytest_json_report_case_count()

    def send_msg(self, msg=''):
        """发送企业微信消息通知"""
        content = f"""
        ******用例执行结果统计******：
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
        > [报告链接]({self.allure_url})
        > [控制台链接]({BUILD_URL})
        {msg}
        """

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
                "mentioned_list": ["汪杰", "@all"],
            },
        }

        for hook_url in self.hook_urls:
            response = requests.post(url=hook_url, headers=self.header, json=payload)
            result = response.json()
            if result["errcode"] == 0:
                print("消息发送成功")
            else:
                print(f"消息发送失败，错误代码：{result['errcode']}，错误信息：{result['errmsg']}")


class RobotSender:

    @staticmethod
    def send_enterprise_wechat(url, msg):
        """发送到企业微信群"""
        url = url
        headers = {"Content-Type": "application/json"}

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg,
                "mentioned_list": ["汪杰", "@all"],
            },
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result["errcode"] == 0:
            print("消息发送成功")
        else:
            print(f"消息发送失败，错误代码：{result['errcode']}，错误信息：{result['errmsg']}")


if __name__ == '__main__':
    # msg = '消息通知：\n' \
    #       '执行人：汪杰\n' \
    #       '通过率：\n' \
    #       '执行结果：\n'
    # RobotSender().send_enterprise_wechat(
    #     'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50ab5cc5-7b5d-4ed0-a95b-ddd5daeeec5c', msg)

    EnterpriseWechatNotification(
        ['https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50ab5cc5-7b5d-4ed0-a95b-ddd5daeeec5c']).send_msg()
