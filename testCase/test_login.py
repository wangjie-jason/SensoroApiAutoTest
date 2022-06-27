#!/usr/bin/python
# -*- coding:utf-8 -*-
import allure
import pytest

from page_api.login import Login
from tools.get_yaml_data import get_yaml_data


class TestLogin:
    data_smsCode = get_yaml_data('datas/smsCode')

    @allure.feature('获取手机号验证码测试')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('mobile, message', data_smsCode)
    # @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_smsCode(self, mobile, message):
        """获取验证码"""
        r = Login().get_sendSms(mobile)['message']
        assert r == message

    data_login = get_yaml_data('datas/login')

    @allure.feature('登录测试')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('mobile,smsCode,message', data_login)
    def test_login(self, mobile, smsCode, message):
        """登录测试"""
        # 登录前先获取手机号验证码
        # Login().get_sendSms('13718395478')
        # 登录测试
        r = Login().login_v1(mobile, smsCode)['message']
        assert r == message
