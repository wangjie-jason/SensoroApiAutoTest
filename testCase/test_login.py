#!/usr/bin/python
# -*- coding:utf-8 -*-
import allure
import pytest

from pageApi.login import Login
from utils.get_yaml_data import get_yaml_data


@allure.feature("登录模块测试用例")
class TestLogin:
    data_smsCode = get_yaml_data('datas/smsCode.yaml')
    params = [(item['case_title'], item['phone'], item['expected']) for item in data_smsCode]

    @allure.story("测试获取验证码")
    @allure.title('{case_title}')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('case_title,phone, message', params)
    # @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_smsCode(self, case_title, phone, message):
        """获取验证码"""
        r = Login().get_sendSms(phone)
        assert r.json()['message'] == message

    data_login = get_yaml_data('datas/login.yaml')
    params = [(item['case_title'],item['phone'], item['smsCode'], item['expected']) for item in data_login]

    @allure.story("测试登录")
    @allure.title('{case_title}')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('case_title,phone,smsCode,message', params)
    def test_login(self,case_title, phone, smsCode, message):
        """登录测试"""
        # 登录前先获取手机号验证码
        Login().get_sendSms('13800000000')
        # 登录测试
        r = Login().login_app_v2(phone, smsCode)
        assert r.json()['message'] == message
