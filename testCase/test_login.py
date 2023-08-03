#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

import allure
import pytest

from configs.dir_path_config import DATAS_DIR
from pageApi.login import Login
from utils.yaml_handle import YamlHandle


@allure.feature("登录模块")
class TestLogin:
    data_smsCode = YamlHandle(DATAS_DIR+os.sep+'smsCode.yaml').read_yaml()
    params = [(item['case_title'], item['expected']) for item in data_smsCode]

    @allure.story("测试获取验证码")
    @allure.title('{case_title}')
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('case_title,message', params)
    @pytest.mark.dependency(name='get_smsCode')
    # @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_smsCode(self, case_title, message):
        """获取验证码"""
        r = "获取验证码成功"
        assert r == message

    data_login = YamlHandle(DATAS_DIR+os.sep+'login.yaml').read_yaml()
    params = [(item['case_title'], item['username'], item['password'], item['expected']) for item in data_login]

    @allure.story("测试登录")
    @allure.title('{case_title}')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('case_title, username, password,message', params)
    @pytest.mark.dependency(depends=["get_smsCode"], scope='class')
    def test_login(self, case_title, username, password, message):
        """登录测试"""
        r = Login().login(username, password)
        assert r.json()['errorMsg'] == message
