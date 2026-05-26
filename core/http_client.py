#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/3/27 14:17
# @Author : wangjie
# @File : http_client.py
# @project : SensoroApiAutoTest
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

from core.config_manager import config
from core.exceptions import ValueTypeError
from core.logger import logger
from core.models import Method
from utils.MIME_type_classifier import get_MIME
from utils.allure_util import allure_attach_text, allure_attach_json, allure_attach_file


class HttpClient:
    """基础类，对请求方法进行二次封装"""

    def __init__(self):
        self._session = requests.Session()

    @staticmethod
    def _make_url(path: str) -> str:
        """整理拼接URL"""
        if path.lower().startswith("http"):
            return path
        host = config.base_url().rstrip("/")
        url = host + "/" + path.lstrip("/")
        return url

    @staticmethod
    def _make_headers(headers) -> dict[Any, Any]:
        """对请求头进行预处理"""
        default_headers = config.default_headers()
        headers = headers or {}
        merged_headers = {**default_headers, **headers}
        return merged_headers

    @staticmethod
    def _make_method(method) -> str:
        """对请求方法进行预处理"""
        try:
            method_enum = Method[method.upper()]
        except KeyError:
            raise ValueTypeError(f"无效的HTTP请求,请检查你的请求方法是否正确：{method}")
        return method_enum.value

    @staticmethod
    def _make_params(input_params) -> dict[str, int | Any]:
        """对请求参数进行预处理"""
        # 在请求参数里默认加上查询范围
        merged_params = {
            # "page": 1,
            # "size": 20,
            # 'startTime': TimeUtil.get_seven_days_ago_time_unix(),
            # 'endTime': TimeUtil.get_current_time_unix(),
            **(input_params or {})
        }
        return merged_params

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

            # 验证和清理文件路径
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"上传文件: {file_path} 不存在")

            try:
                file_name = os.path.basename(file_path)
                mime_type = get_MIME(file_path)
                files[field_name] = (file_name, open(file_path, 'rb'), mime_type)
                with allure.step("上传的附件"):
                    allure_attach_file(file_name, file_path)
            except Exception as e:
                logger.error(f"上传文件 {file_path} 时出错: {e}")
                raise
        return files

    def _request(self, method: str, path: str, headers: dict = None, params: dict = None, data: dict = None,
                 json_data: dict = None,
                 files=None, timeout: int = 30) -> requests.Response:
        """发送http请求，返回response对象"""
        url = self._make_url(path)
        headers = self._make_headers(headers)
        method = self._make_method(method)
        files = self._make_files(files)

        try:
            start_time = time.time()

            response = self._session.request(method=method, url=url, headers=headers, params=params,
                                             data=data, json=json_data, files=files, timeout=timeout)

            duration = time.time() - start_time

            r_uri = self.get_request_url(response)
            r_method = self.get_request_method(response)
            r_headers = self.get_request_headers(response)
            r_body = self.get_request_body(response)
            r_curl = self.request_to_curl(response)
            r_response = self.get_json(response)
            r_duration = duration
            r_response_status_code = self.get_status_code(response)
            r_response_headers = self.get_response_headers(response)
            _log_msg = f"\n{'=' * 50}\n" \
                       f"请求地址：{r_uri}\n" \
                       f"请求方式：{r_method}\n" \
                       f"请求头：{r_headers}\n" \
                       f"请求内容：{r_body}\n" \
                       f"请求curl命令：{r_curl}\n" \
                       f"接口响应内容:{r_response}\n" \
                       f"接口响应头:{r_response_headers}\n" \
                       f"接口响应时长:{r_duration:.2f}秒\n" \
                       f"HTTP状态码：{r_response_status_code}\n" \
                       f"{'=' * 50}\n\n"

            with allure.step("请求内容"):
                allure_attach_text("请求地址", r_uri)
                allure_attach_text("请求方式", r_method)
                allure_attach_json("请求头", r_headers)
                allure_attach_json("请求体", r_body)
                allure_attach_text("请求curl命令", r_curl)
            with allure.step("响应内容"):
                allure_attach_json("响应体", r_response)
                allure_attach_text("HTTP状态码", f"{r_response_status_code}")
                allure_attach_json("响应头", r_response_headers)

            if response.status_code == 200:
                logger.info(_log_msg)
            else:
                logger.error(_log_msg)
            return response
        except Exception as e:
            logger.error(f'发送{method.upper()}请求失败，请求地址为：{url}，错误信息：{e}')
            raise e

    def get(self, path: str, params: dict = None, headers: dict = None,
            timeout: int = 30) -> requests.Response:
        """发送get请求，返回response对象"""
        params = self._make_params(params)
        return self._request(method='get', path=path, params=params, headers=headers, timeout=timeout)

    def post(self, path: str, data: dict = None, json_data: dict = None,
             headers: dict = None, files=None, timeout: int = 30) -> requests.Response:
        """发送post请求，返回response对象"""
        return self._request(method='post', path=path, data=data, json_data=json_data, headers=headers,
                             files=files, timeout=timeout)

    def delete(self, path: str, data: dict = None, json_data: dict = None,
               headers: dict = None, files=None, timeout: int = 30) -> requests.Response:
        """发送delete请求，返回response对象"""
        return self._request(method='delete', path=path, data=data, json_data=json_data, headers=headers,
                             files=files, timeout=timeout)

    def put(self, path: str, data: dict = None, json_data: dict = None,
            headers: dict = None, files=None, timeout: int = 30) -> requests.Response:
        """发送put请求，返回response对象"""
        return self._request(method='put', path=path, data=data, json_data=json_data, headers=headers,
                             files=files, timeout=timeout)

    @staticmethod
    def get_json(response: requests.Response) -> dict | Any:
        """获取响应结果的json格式"""
        try:
            return response.json()
        except json.JSONDecodeError:
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
    def get_request_headers(response: requests.Response) -> dict:
        """获取请求头"""
        return dict(response.request.headers.copy())

    @staticmethod
    def get_response_headers(response: requests.Response) -> dict:
        """获取响应头"""
        return dict(response.headers)

    @staticmethod
    def get_request_body(response: requests.Response) -> str | None:
        """获取请求体内容"""
        request = response.request
        body = request.body
        if isinstance(body, bytes):
            try:
                body = body.decode('utf-8')
            except UnicodeDecodeError:
                body = base64.b64encode(body).decode('utf-8')
        return body

    @staticmethod
    def get_request_info(response: requests.Response) -> Tuple[str, str, str | None, CaseInsensitiveDict[str]]:
        """获取请求的全部信息"""
        request: PreparedRequest = response.request
        headers = request.headers.copy()
        url: str = request.url
        method: str = request.method.upper()
        body: Optional[str] = request.body
        if isinstance(body, bytes):
            try:
                body = body.decode('utf-8')
            except UnicodeDecodeError:
                body = base64.b64encode(body).decode('utf-8')
        return method, url, body, headers

    @staticmethod
    def request_to_curl(response: requests.Response) -> str:
        """将request请求转化为curl命令"""
        try:
            curl = py3curl.request_to_curl(response.request)
            return curl
        except Exception as e:
            logger.error(f"请求中可能存在二进制文件，不建议转成curl,错误信息：{e}")


if __name__ == '__main__':
    path = 'users/1'
    r = HttpClient().get(path)
    print(HttpClient.get_json(r))
