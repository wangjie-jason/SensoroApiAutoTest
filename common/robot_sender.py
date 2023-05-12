# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/5 11:48
# @Author : wangjie
# @File : robot_sender.py
# @project : SensoroApi
import requests
import json

import os
import json
import requests
import platform


def get_env_from_jenkins(name, base=''):
    """从Jenkins中获取全局环境变量"""
    return os.getenv(name) and os.getenv(name).strip() or base


ProjectName = get_env_from_jenkins("JOB_NAME")  # Jenkins构建项目名称
BUILD_URL = get_env_from_jenkins("BUILD_URL")  # Jenkins构建项目URL
BUILD_NUMBER = get_env_from_jenkins("BUILD_NUMBER")  # Jenkins构建编号


class EnterpriseWechatNotification:
    def __init__(self, hook_urls: list):
        # 企业微信群机器人的hook地址，一个机器人就一个，多个就定义多个，可以写死，也可以写在配置类中
        self.hook_urls = hook_urls
        # allure生成报告的地址，Jenkins执行时会用到，Windows暂未配置allure地址
        self.allure_url = f"http://192.168.1.122:8088/jenkins/job/{ProjectName}/{BUILD_NUMBER}/allure/"
        self.header = {'Content-Type': 'application/json'}

    def send_msg(self, result=''):
        """发送企业微信消息通知"""
        global content
        linux_content = f"""** 【{ProjectName}】**
> 项目名称:{ProjectName}
> 构件编号:#{BUILD_NUMBER}
> 测试环境:{platform.system()}
> [报告链接]({self.allure_url})
> [控制台链接]({BUILD_URL})
{result}"""

        windows_content = f"""** 【auto_test_project】**
> 测试环境:{platform.system()}
{result}"""
        if platform.system() == "Linux" or "Darwin":
            content = linux_content
        elif platform.system() == "Windows":
            content = windows_content

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
            },
        }

        for hook_url in self.hook_urls:
            response = requests.post(url=hook_url, headers=self.header, data=json.dumps(payload))
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
                "mentioned_list": ["wangjie", "@all"],
            },
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result["errcode"] == 0:
            print("消息发送成功")
        else:
            print(f"消息发送失败，错误代码：{result['errcode']}，错误信息：{result['errmsg']}")


if __name__ == '__main__':
    msg = '消息通知：\n' \
          '执行人：汪杰\n' \
          '通过率：\n' \
          '执行结果：\n'
    RobotSender().send_enterprise_wechat(
        'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50ab5cc5-7b5d-4ed0-a95b-ddd5daeeec5c', msg)
