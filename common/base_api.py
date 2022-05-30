# !/usr/bin/python
# -*- coding:utf-8 -*-
import configparser
import json
import os

import requests

from common.base_log import Logging

path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(path, '../configs'))


# logger = Logging().get_logger()

class BaseApi:
    """基础类，提供公共方法"""

    def __init__(self):
        """读取环境配置文件"""
        config = configparser.ConfigParser()
        config.read(file_path + '/lins_environment.ini', encoding="utf-8")
        self.host = config
        # 添加日志器
        self.logger = Logging().get_logger()

    def get_(self, address, params=None, header=None, environment='test'):
        """发送get请求，返回json格式数据"""
        try:
            response = requests.get(url=f'{self.host[environment]["host"]}{address}', headers=header,
                                    params=params)
            if response.status_code == 200:
                self.logger.info("测试接口：{}".format(f'{self.host[environment]["host"]}{address}'))
                self.logger.info("响应内容：{}".format(response.json()))
                self.logger.info("响应状态码：{}".format(response.status_code))
                return response.json()
            elif 200 < response.status_code < 400:
                self.logger.info("Redirect_URL: {}".format(response.url))
            elif 400 <= response.status_code < 500:
                self.logger.info("接口请求异常,状态码为：{}".format(response.status_code))
                return response.json()
            else:
                self.logger.info("服务器内部报错,状态码为：{}".format(response.status_code))
        except Exception as e:
            self.logger.error('get请求%s失败，错误信息%s' % (f'{self.host[environment]["host"]}{address}', e))

    def post_(self, address, data=None, json=None, header=None, file=None, environment='test'):
        """发送past请求，返回json格式数据"""
        try:
            response = requests.post(url=self.host[environment]["host"] + address, headers=header,
                                     data=data, json=json, files=file)
            if response.status_code == 200:
                self.logger.info("测试接口：{}".format(f'{self.host[environment]["host"]}{address}'))
                self.logger.info("响应内容：{}".format(response.json()))
                self.logger.info("响应状态码：{}".format(response.status_code))
                return response.json()
            elif 200 < response.status_code < 400:
                self.logger.info("Redirect_URL: {}".format(response.url))
            elif 400 <= response.status_code < 500:
                self.logger.info("接口请求异常,状态码为：{}".format(response.status_code))
                return response.json()
            else:
                self.logger.info("服务器内部报错,状态码为：{}".format(response.status_code))
        except Exception as e:
            self.logger.error('post请求%s失败，错误信息%s' % (f'{self.host[environment]["host"]}{address}', e))

    def delete_(self, address, data=None, json=None, header=None, file=None, environment='test') -> json:
        """发送delete请求，返回json格式数据"""
        try:
            response = requests.delete(url=self.host[environment]["host"] + address, headers=header,
                                       data=data, json=json, files=file)
            if response.status_code == 200:
                self.logger.info("测试接口：{}".format(f'{self.host[environment]["host"]}{address}'))
                self.logger.info("响应内容：{}".format(response.json()))
                self.logger.info("响应状态码：{}".format(response.status_code))
                return response.json()
            elif 200 < response.status_code < 400:
                self.logger.info("Redirect_URL: {}".format(response.url))
            elif 400 <= response.status_code < 500:
                self.logger.info("接口请求异常,状态码为：{}".format(response.status_code))
                return response.json()
            else:
                self.logger.info("服务器内部报错,状态码为：{}".format(response.status_code))
        except Exception as e:
            self.logger.error('delete请求%s失败，错误信息%s' % (f'{self.host[environment]["host"]}{address}', e))

    def put_(self, address, data=None, json=None, header=None, file=None, environment='test') -> json:
        """发送put请求，返回json格式数据"""
        try:
            response = requests.post(url=self.host[environment]["host"] + address, headers=header,
                                     data=data, json=json, files=file)
            if response.status_code == 200:
                self.logger.info("测试接口：{}".format(f'{self.host[environment]["host"]}{address}'))
                self.logger.info("响应内容：{}".format(response.json()))
                self.logger.info("响应状态码：{}".format(response.status_code))
                return response.json()
            elif 200 < response.status_code < 400:
                self.logger.info("Redirect_URL: {}".format(response.url))
            elif 400 <= response.status_code < 500:
                self.logger.info("接口请求异常,状态码为：{}".format(response.status_code))
                return response.json()
            else:
                self.logger.info("服务器内部报错,状态码为：{}".format(response.status_code))
        except Exception as e:
            self.logger.error('put请求%s失败，错误信息%s' % (f'{self.host[environment]["host"]}{address}', e))


if __name__ == '__main__':
    address = 'https://lins-test1-api.sensoro.com/auth/v1/sendSms'
    params = {
        'mobile': '13718395478',
        'region': 'CN'}
    BaseApi().get_(address, params=params)
