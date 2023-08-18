# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/3/27 14:17
# @Author : wangjie
# @File : base_api.py
# @project : SensoroApi
import base64
import json
import time
from typing import Optional, Tuple, Dict, Any

import py3curl
import requests
from requests import PreparedRequest
from requests.structures import CaseInsensitiveDict

from common.base_log import logger
from common.exceptions import ValueNotFoundError
from configs.lins_environment import EntryPoint
from utils.time_utils import TimeUtil


class BaseApi:
    """基础类，对请求方法进行二次封装"""

    host = EntryPoint.URL()
    default_headers = EntryPoint.DEFAULT_HEADERS()

    @staticmethod
    def _make_url(address: str) -> str:
        """整理拼接URL"""
        return BaseApi.host + address

    @staticmethod
    def _make_headers(headers) -> dict[Any, Any]:
        """对请求头进行预处理"""
        headers = headers or {}
        headers = {**BaseApi.default_headers, **headers}
        return headers

    @staticmethod
    def _make_method(method) -> str:
        """对请求方法进行预处理"""
        return method.lower()

    @staticmethod
    def _make_params(params) -> dict[str, int | Any]:
        """对请求参数进行预处理"""
        params = params or {}
        # 在请求参数里默认加上查询范围
        params = {
            "page": 1,
            "size": 20,
            'startTime': TimeUtil.get_current_time_unix(),
            'endTime': TimeUtil.get_seven_days_ago_time_unix(),
            **params
        }
        return params

    @staticmethod
    def request(method, address, headers=None, params=None, data=None, json=None, files=None) -> requests.Response:
        """发送http请求，返回response对象"""
        # 处理请求参数
        url = BaseApi._make_url(address)
        headers = BaseApi._make_headers(headers)
        method = BaseApi._make_method(method)

        # 发送请求
        try:
            start_time = time.time()  # 记录请求开始时间
            # 发起请求
            response = requests.request(method=method, url=url, headers=headers, params=params,
                                        data=data, json=json, files=files)
            end_time = time.time()  # 记录请求结束时间
            elapsed_time = end_time - start_time  # 计算请求时长
            # 记录请求时的详情信息
            _log_msg = f"\n==================================================\n" \
                       f"请求路径：{response.request.url}\n" \
                       f"请求方式：{method.upper()}\n" \
                       f"请求头：{response.request.headers}\n" \
                       f"请求内容：{BaseApi.get_request_body(response)}\n" \
                       f"请求curl命令：{BaseApi.request_to_curl(response)}\n" \
                       f"接口响应内容:{response.json()}\n" \
                       f"接口响应时长:{elapsed_time:.2f}秒\n" \
                       f"HTTP状态码：{response.status_code}\n" \
                       f"=================================================="
            if response.status_code == 200:
                logger.info(_log_msg)
            else:
                logger.error(_log_msg)
            return response
        except Exception as e:
            logger.error(f'发送{method.upper()}请求失败，请求接口为：{url}，错误信息：{e}')
            raise e

    @staticmethod
    def get(address, params=None, headers=None) -> requests.Response:
        """发送get请求，返回response对象"""
        # get请求会默认带上查询范围的参数
        params = BaseApi._make_params(params)
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
            raise ValueNotFoundError('请求返回结果为空，无法获取响应')

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
    def get_request_url(response: requests.Response) -> str:
        """获取请求完整url"""
        return response.request.url

    @staticmethod
    def get_request_method(response: requests.Response) -> str:
        """获取请求方式"""
        return response.request.method.upper()

    @staticmethod
    def get_request_headers(response: requests.Response) -> CaseInsensitiveDict[str]:
        """获取请求头"""
        request = response.request
        headers = request.headers.copy()
        headers.pop('User-Agent', None)
        return headers

    @staticmethod
    def get_request_body(response: requests.Response) -> str | None:
        """获取请求体内容"""
        request = response.request
        body = request.body
        if isinstance(body, bytes):
            try:  # 请求体是文本就直接将其解码为 UTF-8 编码的字符串
                body = body.decode('utf-8')
            except UnicodeDecodeError:  # 否则将其编码为 base64 编码的字符串。
                body = base64.b64encode(body).decode('utf-8')
        return body

    @staticmethod
    def get_request_info(response: requests.Response) -> Tuple[str, str, str | None, CaseInsensitiveDict[str]]:
        """获取请求的全部信息"""
        request: PreparedRequest = response.request
        headers = request.headers.copy()
        headers.pop('User-Agent', None)
        url: str = request.url
        method: str = request.method.upper()
        body: Optional[str] = request.body
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
            return logger.error(f"请求中可能存在二进制文件，不建议转成curl,错误信息：{e}")


if __name__ == '__main__':
    address = 'auth/v1/sendSms'
    params = {
        'mobile': '13800000000',
        'region': 'CN'}
    r = BaseApi.get(address, params=params)
    print(BaseApi.get_request_info(r))
