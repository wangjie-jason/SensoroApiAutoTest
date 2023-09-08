# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/5 11:48
# @Author : wangjie
# @File : robot_sender.py
# @project : SensoroApi

import requests
from common.base_log import logger
from common.exceptions import SendMessageError, ValueTypeError


class EnterpriseWechatNotification:
    """企业微信群通知"""

    def __init__(self, hook_urls: list):
        # 企业微信群机器人的hook地址，一个机器人就一个，多个就定义多个，可以写死，也可以写在配置类中
        self.hook_urls = hook_urls
        self.header = {'Content-Type': 'application/json'}

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

    def send_markdown(self, content):
        """
        发送markdown消息
        :param content: markdown格式内容
        :return:
        """
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

        logger.info("开始发送企业微信消息")

        payload = payload

        for hook_url in self.hook_urls:
            response = requests.post(url=hook_url, headers=self.header, json=payload)
            result = response.json()
            if result["errcode"] == 0:
                logger.info("企业微信消息发送成功")
            else:
                logger.error(f'企业微信「{payload["msgtype"]}类型」消息发送失败：{response.json()}')
                raise SendMessageError(
                    f"企业微信「{payload['msgtype']}类型」消息发送失败，错误代码：{result['errcode']}，错误信息：{result['errmsg']}")


if __name__ == '__main__':
    EnterpriseWechatNotification(
        ['hook_url']).send_markdown('<@汪杰>')
