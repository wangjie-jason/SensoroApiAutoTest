# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi
import allure
import pytest

from common.base_api import BaseApi
from common.base_log import logger
from common.exceptions import ValueNotFoundError
from pageApi.login import Login
from utils.allure_handle import allure_attach_text

# 定义一个全局变量，用于存储提取的参数内容
_global_data = {}


@pytest.fixture(scope="session", autouse=False)
def set_global_data():
    """
    设置全局变量，用于关联参数
    :return:
    """

    def _set_global_data(cache_name, value):
        _global_data[cache_name] = value
        with allure.step("提取"):
            allure_attach_text("设置变量", str(f"'{cache_name}':'{value}'"))
            allure_attach_text("当前可使用的全局变量", str(_global_data))

    yield _set_global_data
    _global_data.clear()


@pytest.fixture(scope="session", autouse=False)
def get_global_data():
    """
    从全局变量global_data中取值
    :return:
    """

    def _get_global_data(cache_data):
        try:
            with allure.step("提取"):
                allure_attach_text("取出来的变量", str(f"{cache_data}:{_global_data.get(cache_data, None)}"))
            return _global_data[cache_data]
        except KeyError:
            with allure.step("获取变量失败，当前可使用的全局变量"):
                allure_attach_text("获取变量失败，当前可使用的全局变量", str(_global_data))
            raise ValueNotFoundError(f"{cache_data}的缓存数据未找到，请检查是否将该数据存入缓存中")

    return _get_global_data


@pytest.fixture(scope="session", autouse=False)
def get_token():
    """获取登录V1的token"""
    logger.info("开始用例前置操作")
    # 调登录接口，获取登录接口的token¬
    login_response = Login().login('18800000001', '123456')
    token = BaseApi.get_json(login_response)['data']['token']
    logger.info("结束用例前置操作")
    return token
