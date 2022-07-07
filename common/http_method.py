# !/usr/bin/python
# -*- coding:utf-8 -*-
import json

import requests

from common.base_log import Logger
from configs.lins_environment import EntryPoint


class BaseApi:
    """基础类，对请求方法进行二次封装"""

    def __init__(self):
        """读取环境配置"""
        # 获取待测试的环境域名
        self.host = EntryPoint().URL
        # 添加日志器
        self.logger = Logger().get_logger()

    def get_(self, address, params=None, headers=None):
        """发送get请求，返回json格式数据"""
        try:
            response = requests.get(url=self.host + address, headers=headers,
                                    params=params)
            if response.status_code == 200:
                self.logger.info("发送get请求成功，请求接口为：{}".format(f'{self.host}{address}'))
                self.logger.info("响应状态码：{}".format(response.status_code))
            else:
                self.logger.info("发送get请求失败，请求接口为：{}".format(f'{self.host}{address}'))
                self.logger.info("响应状态码：{}".format(response.status_code))
                self.logger.info("响应内容：{}".format(response.json()))
            return response
        except Exception as e:
            self.logger.error('发送get请求失败，请求接口为：%s，错误信息：%s' % (f'{self.host}{address}', e))

    def post_(self, address, data=None, json=None, headers=None, files=None):
        """发送past请求，返回json格式数据"""
        try:
            response = requests.post(url=self.host + address, headers=headers,
                                     data=data, json=json, files=files)
            if response.status_code == 200:
                self.logger.info("发送post请求成功，请求接口为：{}".format(f'{self.host}{address}'))
                self.logger.info("响应状态码：{}".format(response.status_code))
            else:
                self.logger.info("发送post请求失败，请求接口为：{}".format(f'{self.host}{address}'))
                self.logger.info("响应状态码：{}".format(response.status_code))
                self.logger.info("响应内容：{}".format(response.json()))
            return response
        except Exception as e:
            self.logger.error('发送post请求失败，请求接口为：%s，错误信息：%s' % (f'{self.host}{address}', e))


def delete_(self, address, data=None, json=None, headers=None, files=None) -> json:
    """发送delete请求，返回json格式数据"""
    try:
        response = requests.delete(url=self.host + address, headers=headers,
                                   data=data, json=json, files=files)
        if response.status_code == 200:
            self.logger.info("发送delete请求成功，请求接口为：{}".format(f'{self.host}{address}'))
            self.logger.info("响应状态码：{}".format(response.status_code))
        else:
            self.logger.info("发送delete请求失败，请求接口为：{}".format(f'{self.host}{address}'))
            self.logger.info("响应状态码：{}".format(response.status_code))
            self.logger.info("响应内容：{}".format(response.json()))
        return response
    except Exception as e:
        self.logger.error('发送delete请求失败，请求接口为：%s，错误信息：%s' % (f'{self.host}{address}', e))


def put_(self, address, data=None, json=None, headers=None, files=None) -> json:
    """发送put请求，返回json格式数据"""
    try:
        response = requests.post(url=self.host + address, headers=headers,
                                 data=data, json=json, files=files)
        if response.status_code == 200:
            self.logger.info("发送put请求成功，请求接口为：{}".format(f'{self.host}{address}'))
            self.logger.info("响应状态码：{}".format(response.status_code))
        else:
            self.logger.info("发送put请求失败，请求接口为：{}".format(f'{self.host}{address}'))
            self.logger.info("响应状态码：{}".format(response.status_code))
            self.logger.info("响应内容：{}".format(response.json()))
        return response
    except Exception as e:
        self.logger.error('发送put请求失败，请求接口为：%s，错误信息：%s' % (f'{self.host}{address}', e))


if __name__ == '__main__':
    address = 'auth/v1/sendSms'
    params = {
        'mobile': '13718395478',
        'region': 'CN'}
    BaseApi().get_(address, params=params)
