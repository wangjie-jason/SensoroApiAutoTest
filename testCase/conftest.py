# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi
import os.path
import platform

import allure
import pytest
from py.xml import html

from common.http_method import BaseApi
from common.settings import ENV
from configs.dir_path_config import BASE_DIR
from pageApi.login import Login

# 定义一个全局变量，用于存储提取的参数内容
global_data = {}


@pytest.fixture(scope="session", autouse=False)
def set_global_data():
    """
    设置全局变量，用于关联参数
    :return:
    """

    def _set_global_data(key, value):
        global_data[key] = value
        allure.attach(str(f"'{key}':'{value}'"), '设置变量：', allure.attachment_type.TEXT)
        allure.attach(str(global_data), '当前可使用的全局变量：', allure.attachment_type.TEXT)

    yield _set_global_data
    global_data.clear()


@pytest.fixture(scope="session", autouse=False)
def get_global_data():
    """
    从全局变量global_data中取值
    :return:
    """

    def _get_global_data(key):
        allure.attach(str(f"{key}:{global_data.get(key, None)}"), '取出来的变量：', allure.attachment_type.TEXT)
        return global_data.get(key, None)

    return _get_global_data


@pytest.fixture(scope="session", autouse=False)
def get_token():
    """获取登录V1的token"""
    # 登录前需要先获取验证码
    Login().get_sendSms('13800000000')
    # 调登录接口，获取登录接口的token¬
    login_response = Login().login_v1('13800000000', '138000')
    token = BaseApi.get_json(login_response)['data']['token']
    return token


@pytest.fixture(scope="session", autouse=False)
def get_token_v2():
    """获取登录V2的Ai视频管理项目的token"""
    # 登录前需要先获取验证码
    Login().get_sendSms('13800000000')
    # 调登录接口，获取登录接口的token
    login_response = Login().login_app_v2('13800000000', '138000')
    login_token = BaseApi.get_json(login_response)['data']['token']
    # 调切换租户的接口，获取切换到指定租户的token
    headers = {'Authorization': f'Bearer {login_token}'}
    res = Login().select_tenant(tenantId='1622903542623612930', projectId='1622903550156582913', headers=headers)
    token = BaseApi.get_json(res)['data']['token']
    return token