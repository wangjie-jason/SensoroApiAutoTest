# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/3/27 14:17
# @Author : wangjie
# @File : base_api.py
# @project : SensoroApi
import base64
import json
import os
import time
from typing import Optional, Tuple, Any, Union, Dict

import allure
import py3curl
import requests
from requests import PreparedRequest
from requests.structures import CaseInsensitiveDict

from common.base_log import logger
from common.exceptions import ValueTypeError
from common.models import Method
from configs.lins_environment import EntryPoint
from utils.MIME_type_classifier import get_MIME
from utils.allure_handle import allure_attach_text, allure_attach_json, allure_attach_file
from utils.time_utils import TimeUtil


class BaseApi:
    """基础类，对请求方法进行二次封装"""

    @staticmethod
    def _make_url(address: str) -> str:
        """整理拼接URL"""
        # 如果address是以http开头的，则直接使用该address，不与host进行拼接
        if address.lower().startswith("http"):
            return address
        # 确保host不以/结尾
        host = EntryPoint.URL().rstrip("/")
        # 确保address是以/开头
        address = "/" + address.lstrip("/")

        return f"{host}{address}"

    @staticmethod
    def _make_headers(headers) -> dict[Any, Any]:
        """对请求头进行预处理"""
        default_headers = EntryPoint.DEFAULT_HEADERS()
        headers = headers or {}
        merged_headers = {**default_headers, **headers}
        return merged_headers

    @staticmethod
    def _make_method(method) -> str:
        """对请求方法进行预处理"""
        # 检查传入的method是否在Method枚举中
        try:
            method_enum = Method[method.upper()]
        except KeyError:
            raise ValueTypeError(f"无效的HTTP请求,请检查你的请求方法是否正确：{method}")
        return method_enum.value

    @staticmethod
    def _make_params(params) -> dict[str, int | Any]:
        """对请求参数进行预处理"""
        params = params or {}
        # 在请求参数里默认加上查询范围
        params = {
            "page": 1,
            "size": 20,
            'startTime': TimeUtil.get_seven_days_ago_time_unix(),
            'endTime': TimeUtil.get_current_time_unix(),
            **params
        }
        return params

    @staticmethod
    def _make_files(files_info: Union[str, Dict[str, str]]) -> Dict[str, Tuple[str, Any, str]]:
        """
        对上传文件进行预处理
        :param files_info: 支持str和dict两种传参方式，str时只需要传文件名即可，该文件字段名默认为file，如果后端要求字段名不是file，可以字典的方式传入k是字段名，v是文件路径，如：{"file":'/Users/wangjie/Desktop/111.png'}
        :return:
        """
        if files_info is None:
            return {}
        # 类型检查
        if not isinstance(files_info, (str, dict)):
            raise TypeError("files_info必须是字符串或字典")

        # 如果传入的是单个文件路径，转换为包含该路径的字典，并带上默认字段名file
        if isinstance(files_info, str):
            files_info = {'file': files_info}

        # 准备上传文件的数据
        files = {}
        for field_name, file_path in files_info.items():
            if not isinstance(field_name, str) or not isinstance(file_path, str):
                raise TypeError("files_info字典中的每个条目必须是一个字符串键和一个字符串值")
            file_name = os.path.basename(file_path)
            files[field_name] = (file_name, open(file_path, 'rb'), get_MIME(file_path))
            with allure.step("上传的附件"):
                allure_attach_file(file_name, file_path)
        return files

    @staticmethod
    def request(method, address, headers=None, params=None, data=None, json_data=None, files=None) -> requests.Response:
        """发送http请求，返回response对象"""
        # 处理请求参数
        url = BaseApi._make_url(address)
        headers = BaseApi._make_headers(headers)
        method = BaseApi._make_method(method)
        files = BaseApi._make_files(files)

        # 发送请求
        try:
            start_time = time.time()  # 记录请求开始时间
            # 发起请求
            response = requests.request(method=method, url=url, headers=headers, params=params,
                                        data=data, json=json_data, files=files)
            end_time = time.time()  # 记录请求结束时间
            duration = end_time - start_time  # 计算请求时长
            # 记录请求时的详情信息
            r_uri = response.request.url
            r_method = method.upper()
            r_headers = response.request.headers
            r_body = BaseApi.get_request_body(response)
            r_curl = BaseApi.request_to_curl(response)
            r_respone = BaseApi.get_json(response)
            r_duration = duration
            r_respone_status_code = response.status_code
            r_respone_headers = response.headers
            _log_msg = f"\n==================================================\n" \
                       f"请求路径：{r_uri}\n" \
                       f"请求方式：{r_method}\n" \
                       f"请求头：{r_headers}\n" \
                       f"请求内容：{r_body}\n" \
                       f"请求curl命令：{r_curl}\n" \
                       f"接口响应内容:{r_respone}\n" \
                       f"接口响应头:{r_respone_headers}\n" \
                       f"接口响应时长:{r_duration:.2f}秒\n" \
                       f"HTTP状态码：{r_respone_status_code}\n" \
                       f"=================================================="
            with allure.step("请求内容"):
                allure_attach_text("请求路径", f"{r_uri}")
                allure_attach_text("请求方式", f"{r_method}")
                allure_attach_text("请求头", f"{r_headers}")
                allure_attach_json("请求体", f"{r_body}")
                allure_attach_text("请求curl命令", f"{r_curl}")
            with allure.step("响应内容"):
                allure_attach_json("响应体", f"{json.dumps(r_respone, ensure_ascii=False, indent=4)}")
                allure_attach_text("HTTP状态码", f"{r_respone_status_code}")
                allure_attach_text("响应头", f"{r_respone_headers}")

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
    def post(address, data=None, json_data=None, headers=None, files=None) -> requests.Response:
        """发送post请求，返回response对象"""
        return BaseApi.request(method='post', address=address, data=data, json_data=json_data, headers=headers,
                               files=files)

    @staticmethod
    def delete(address, data=None, json=None, headers=None, files=None) -> requests.Response:
        """发送delete请求，返回response对象"""
        return BaseApi.request(method='delete', address=address, data=data, json_data=json, headers=headers,
                               files=files)

    @staticmethod
    def put(address, data=None, json_data=None, headers=None, files=None) -> requests.Response:
        """发送put请求，返回response对象"""
        return BaseApi.request(method='put', address=address, data=data, json_data=json_data, headers=headers,
                               files=files)

    @staticmethod
    def get_json(response: requests.Response) -> Union[Dict[str, Any], str]:
        """获取响应结果的json格式"""
        try:
            json_data = response.json()
            return json_data
        except json.JSONDecodeError:
            # 如果json解析失败，则返回原始响应体文本
            return f'解码JSON失败或响应为空,返回原始响应:{response.text}'

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
