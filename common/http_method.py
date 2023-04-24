# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/3/27 14:17
# @Author : wangjie
# @File : http_method.py
# @project : SensoroApi
import base64
import json

import py3curl
import requests
from requests import PreparedRequest
from common.base_log import Logger
from configs.lins_environment import EntryPoint


class BaseApi:
    """基础类，对请求方法进行二次封装"""

    host = EntryPoint.URL()
    default_headers = EntryPoint.DEFAULT_HEADERS()
    logger = Logger().get_logger()

    @staticmethod
    def _get_url(address: str) -> str:
        """拼接URL"""
        return BaseApi.host + address

    @staticmethod
    def _get_headers(headers):
        """获取请求头"""
        headers = headers or {}
        headers = {**BaseApi.default_headers, **headers}
        return headers

    @staticmethod
    def _get_method(method):
        """获取请求方法"""
        return method.lower()

    @staticmethod
    def request(method, address, headers=None, params=None, data=None, json=None, files=None) -> requests.Response:
        """发送http请求，返回response对象"""
        # 处理请求参数
        url = BaseApi._get_url(address)
        headers = BaseApi._get_headers(headers)
        method = BaseApi._get_method(method)

        # 发送请求
        try:
            response = requests.request(method=method, url=url, headers=headers, params=params,
                                        data=data, json=json, files=files)
            if response.status_code == 200:
                BaseApi.logger.info(f"发送{method.upper()}请求成功，请求接口为：{url}")
                BaseApi.logger.info(f"响应状态码：{response.status_code}")
            else:
                BaseApi.logger.info(f"发送{method.upper()}请求失败，请求接口为：{url}")
                BaseApi.logger.info(f"请求内容：{BaseApi.get_request_info(response)}")
                BaseApi.logger.info(f'请求curl命令：{BaseApi.request_to_curl(response)}')
                BaseApi.logger.info(f"响应状态码：{response.status_code}")
                BaseApi.logger.info(f"响应内容：{response.json()}")
            return response
        except Exception as e:
            BaseApi.logger.error(f'发送{method.upper()}请求失败，请求接口为：{url}，错误信息：{e}')
            raise e

    @staticmethod
    def get(address, params=None, headers=None) -> requests.Response:
        """发送get请求，返回response对象"""
        return BaseApi.request(method='get', address=address, params=params, headers=headers)

    @staticmethod
    def post(address, data=None, json=None, headers=None, files=None) -> requests.Response:
        """发送post请求，返回response对象"""
        return BaseApi.request(method='post', address=address, data=data, json=json, headers=headers, files=files)

    @staticmethod
    def delete(address, data=None, json=None, headers=None, files=None) -> requests.Response:
        """发送delete请求，返回response对象"""
        return BaseApi.request(method='delete', address=address, data=data, json=json, headers=headers, files=files)

    @staticmethod
    def put(address, data=None, json=None, headers=None, files=None) -> requests.Response:
        """发送put请求，返回response对象"""
        return BaseApi.request(method='put', address=address, data=data, json=json, headers=headers, files=files)

    @staticmethod
    def get_json(response: requests.Response) -> json:
        """获取响应结果的json格式"""
        if response:
            json_data = response.json()
            return json_data
        else:
            raise Exception('请求返回结果为空')

    @staticmethod
    def get_text(response: requests.Response) -> str:
        """获取响应结果的文本格式"""
        return response.text

    @staticmethod
    def get_status_code(response: requests.Response) -> int:
        """获取响应状态码"""
        return response.status_code

    @staticmethod
    def get_request(response: requests.Response) -> PreparedRequest:
        """获取请求对象"""
        return response.request

    @staticmethod
    def get_request_info(response: requests.Response) -> tuple:
        """获取请求内容"""
        request = response.request
        headers = request.headers.copy()
        headers.pop('User-Agent', None)
        url = request.url
        method = request.method.upper()
        body = request.body
        if isinstance(body, bytes):
            try:  # 请求体是文本就直接将其解码为 UTF-8 编码的字符串
                body = body.decode('utf-8')
            except UnicodeDecodeError:  # 否则将其编码为 base64 编码的字符串。
                body = base64.b64encode(body).decode('utf-8')
        return method, url, body, headers

    @staticmethod
    def request_to_curl(response: requests.Response) -> str:
        """将request请求转化为curl命令"""
        try:
            curl = py3curl.request_to_curl(response.request)
            return curl
        except Exception as e:
            return BaseApi.logger.info(f"请求中可能存在二进制文件，不建议转成curl,错误信息：{e}")


if __name__ == '__main__':
    address = 'auth/v1/sendSms'
    params = {
        'mobile': '13800000000',
        'region': 'CN'}
    r = BaseApi.get(address, params=params)
    print(BaseApi.get_request_info(r))
