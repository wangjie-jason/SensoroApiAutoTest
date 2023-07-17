#!/usr/bin/python
# -*- coding:utf-8 -*-
import allure
import pytest

from pageApi.login import Login
from utils.yaml_handle import YamlHandle


@allure.feature("登录模块")
class TestLogin:
    data_smsCode = YamlHandle('datas/smsCode.yaml').read_yaml()
    params = [(item['case_title'], item['phone'], item['expected']) for item in data_smsCode]

    @allure.story("测试获取验证码")
    @allure.title('{case_title}')
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('case_title,phone, message', params)
    @pytest.mark.dependency(name='get_smsCode')
    # @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_smsCode(self, case_title, phone, message):
        """获取验证码"""
        r = Login().get_sendSms(phone)
        assert r.json()['message'] == message

    data_login = YamlHandle('datas/login.yaml').read_yaml()
    params = [(item['case_title'], item['phone'], item['smsCode'], item['expected']) for item in data_login]

    @allure.story("测试登录")
    @allure.title('{case_title}')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('case_title,phone,smsCode,message', params)
    @pytest.mark.dependency(depends=["get_smsCode"], scope='class')
    def test_login(self, case_title, phone, smsCode, message):
        """登录测试"""
        r = Login().login_app_v2(phone, smsCode)
        assert r.json()['message'] == message
