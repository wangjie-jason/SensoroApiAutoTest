# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/5 11:48
# @Author : wangjie
# @File : robot_sender.py
# @project : SensoroApi

import os
import requests

from common.base_log import Logger
from common.exceptions import SendMessageError, ValueTypeError
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

    def send_text(self, content, mentioned_mobile_list=None):
        """
        发送文本类型通知
        :param content: 文本内容，最长不超过2048个字节，必须是utf8编码
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """
        payload = {"msgtype": "text",
                   "text": {
                       "content": content,
                       "mentioned_list": None,
                       "mentioned_mobile_list": mentioned_mobile_list}}

        if mentioned_mobile_list is None or isinstance(mentioned_mobile_list, list):
            # 判断手机号码列表中得数据类型，如果为int类型，发送得消息会乱码
            if len(mentioned_mobile_list) >= 1:
                for i in mentioned_mobile_list:
                    if isinstance(i, str):
                        self._send_msg(payload)
                    else:
                        raise ValueTypeError("手机号码必须是字符串类型.")
        else:
            raise ValueTypeError("手机号码列表必须是list类型.")

    def send_markdown(self, content=''):
        """
        发送markdown消息
        :param content: markdown格式内容
        :return:
        """
        content = f"""******用例执行结果统计******
                > 项目名称:{ProjectName}
                > 构件编号:#{BUILD_NUMBER}
                > 测试环境:{ENV.name}
                > 总用例数：<font color=\"info\">{self.pytest_result['total_case']}条</font>
                > 通过用例数：<font color=\"info\">{self.pytest_result['pass_case']}条</font>
                > 失败用例数：<font color=\"warning\">{self.pytest_result['fail_case']}条</font>
                > 报错用例数：<font color=\"warning\">{self.pytest_result['error_case']}条</font>
                > 跳过用例数：<font color=\"comment\">{self.pytest_result['skip_case']}条</font>
                > 预期失败用例数：<font color=\"comment\">{self.pytest_result['xfail_case']}条</font>
                > 预期通过用例数：<font color=\"comment\">{self.pytest_result['xpass_case']}条</font>
                > 通过率：<font color=\"info\">{self.pytest_result['pass_rate']}%</font>
                > 用例执行时间：<font color=\"info\">{self.pytest_result['case_duration']}s</font>
                > 测试报告，点击查看>>[测试报告入口]({ALLURE_URL})
                > 构建详情，点击查看>>[控制台入口]({BUILD_URL})
                > {content}"""

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
            },
        }
        self._send_msg(payload)

    def _upload_file(self, file):
        """
        先将文件上传到临时媒体库
        """
        for hook_url in self.hook_urls:
            key = hook_url.split("key=")[1]
            url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
            data = {"file": open(file, "rb")}
            res = requests.post(url, files=data).json()
            return res['media_id']

    def send_file_msg(self, file):
        """
        发送文件类型的消息
        @return:
        """

        payload = {"msgtype": "file",
                   "file": {"media_id": self._upload_file(file)}
                   }
        self._send_msg(payload)

    def _send_msg(self, payload):
        """发送企业微信消息通知"""
        logger = Logger().get_logger()

        payload = payload

        for hook_url in self.hook_urls:
            response = requests.post(url=hook_url, headers=self.header, json=payload)
            result = response.json()
            if result["errcode"] == 0:
                logger.info("企业微信消息发送成功")
            else:
                logger.error(f'企业微信「{payload["msgtype"]}类型」消息发送失败：{response.json()}')
                raise SendMessageError(f"企业微信「MarkDown类型」消息发送失败，错误代码：{result['errcode']}，错误信息：{result['errmsg']}")


if __name__ == '__main__':
    EnterpriseWechatNotification(
        ['https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3c5089f8-79b3-4ddd-9d55-f64464f838f9']).send_markdown(
        '<@汪杰>')
