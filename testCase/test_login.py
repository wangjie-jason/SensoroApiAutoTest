#!/usr/bin/python
# -*- coding:utf-8 -*-
import allure
import pytest

from page_api.login import Login
from tools.get_yaml_data import get_yaml_data


class TestLogin():
    data = get_yaml_data('datas/login')

    @allure.feature('登录测试')
    @pytest.mark.parametrize('mobile,smsCode,message', data)
    def test_login(self, mobile, smsCode, message):
        """登录测试"""
        data = {
            'method': 'get',
            'url': f'{get_yaml_data("configs/lins_test1")["host"]}auth/v1/sendSms',
            'params': {
                'mobile': '13718395478',
                'region': 'CN'
            }
        }
        Login().get_sendSms(data)
        data = {
            'method': 'post',
            'url': f'{get_yaml_data("configs/lins_test1")["host"]}auth/v1/loginByMobile',
            'json': {
                'sessionId': "018pT9kOhM2HyUciiIhkMNQW3X22EydkN2ZSG3_h26UhsRJPOUCUAJfFzae-5_k_cU0Auw03ocNqlFM_dWbIWZE1OCFecobl9BvRfCBJTS1_lypbdxU97CpNssyX9kcqkv",
                'sig': "05XqrtZ0EaFgmmqIQes-s-CAiu5y6YBKaSb9AKSL5UbzpDSilBMvhSwiXdbW4r0pATPpuHcErPtBVQb4T02lxA-qXfhyddfcu1iWhmGu9QsPK57UVcRnFNnulf2Qcn6OK7F4X3BvT9lmcJ1pFVxew7PyNaG1nrqsFKgXWTIfKDE5txdIp6Dpd_xDkUZUaCuDHKFZO3KxUTrusHohfcRFSf3vTfA5EQEfyztOrWkZW-NGoUjgPgQvLzTpWSOm2JCTNmfoCOZltk2IX8EXfWk-56-z0AFHvU-jDkqi0udtdeDrveaNYC7kddMKqCOML4fNgMQwi6wQHVvY6Rh5yNKBcihg",
                'token': "1648286210510:0.5175585315118147",
                'scene': "ic_login",
                'appKey': "FFFF0N00000000008D02",
                'mobile': mobile,
                'smsCode': smsCode,
                'region': "CN"

            }
        }
        r = Login().login(data)
        assert r == message
        print(r)
