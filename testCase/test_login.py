#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

import allure
import pytest

from common.base_api import BaseApi
from configs.paths_config import DATAS_DIR
from pageApi.login import Login
from utils.allure_handle import allure_attach_json
from utils.yaml_handle import YamlHandle


@allure.feature("登录模块")
class TestLogin:
    """测试登录相关功能"""
    # 加载测试数据
    data_sms_code = YamlHandle(DATAS_DIR + os.sep + 'sms_code.yaml').read_yaml()
    params_sms = [(item['case_title'], item['expected']) for item in data_sms_code]

    data_login = YamlHandle(DATAS_DIR + os.sep + 'login.yaml').read_yaml()
    params_login = [(item['case_title'], item['username'], item['password'], item['expected']) for item in data_login]

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("测试获取验证码")
    @allure.title('{case_title}')
    @allure.description("""
            测试获取短信验证码接口:
            1. 验证接口是否正常返回
            2.  验证错误提示信息
        """)
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('case_title,message', params_sms)
    @pytest.mark.dependency(name='get_sms_code')
    # @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_sms_code(self, case_title, message):
        """获取验证码"""
        with allure.step("准备请求数据"):
            allure_attach_json("请求参数", {"message": message})

        with allure.step("验证响应结果"):
            response = "获取验证码成功"
            assert response == message

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("测试登录")
    @allure.title('{case_title}')
    @allure.description("""
            测试用户登录接口:
            1. 验证接口是否正常返回
            2. 验证错误场景处理
        """)
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('case_title, username, password,message', params_login)
    @pytest.mark.dependency(depends=["get_sms_code"], scope='class')
    def test_login(self, case_title, username, password, message):
        """登录测试"""
        with allure.step("准备登录请求数据"):
            login_data = {
                "username": username,
                "password": password
            }
            allure_attach_json("请求参数", login_data)

        with allure.step("发送登录请求"):
            response = Login.login(username, password)

        with allure.step("验证响应结果"):
            response_data = BaseApi.get_json(response)
            assert response_data['errorMsg'] == message, f"接口返回错误：{response_data['message']}"
