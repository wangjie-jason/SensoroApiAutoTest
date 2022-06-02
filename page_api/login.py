#!/usr/bin/python
# -*- coding:utf-8 -*-
from common.http_method import BaseApi


class Login(BaseApi):
    """登录模块"""

    def get_sendSms(self, mobile):
        """获取手机号验证码"""
        address = 'auth/v1/sendSms'
        params = {
            'mobile': mobile,
            'region': 'CN'}

        return self.get_(address, params=params)

    def login(self, mobile, smsCode):
        """登录"""
        address = 'auth/v1/loginByMobile'
        json = {
            'sessionId': "018pT9kOhM2HyUciiIhkMNQW3X22EydkN2ZSG3_h26UhsRJPOUCUAJfFzae-5_k_cU0Auw03ocNqlFM_dWbIWZE1OCFecobl9BvRfCBJTS1_lypbdxU97CpNssyX9kcqkv",
            'sig': "05XqrtZ0EaFgmmqIQes-s-CAiu5y6YBKaSb9AKSL5UbzpDSilBMvhSwiXdbW4r0pATPpuHcErPtBVQb4T02lxA-qXfhyddfcu1iWhmGu9QsPK57UVcRnFNnulf2Qcn6OK7F4X3BvT9lmcJ1pFVxew7PyNaG1nrqsFKgXWTIfKDE5txdIp6Dpd_xDkUZUaCuDHKFZO3KxUTrusHohfcRFSf3vTfA5EQEfyztOrWkZW-NGoUjgPgQvLzTpWSOm2JCTNmfoCOZltk2IX8EXfWk-56-z0AFHvU-jDkqi0udtdeDrveaNYC7kddMKqCOML4fNgMQwi6wQHVvY6Rh5yNKBcihg",
            'token': "1648286210510:0.5175585315118147",
            'scene': "ic_login",
            'appKey': "FFFF0N00000000008D02",
            'mobile': mobile,
            'smsCode': smsCode,
            'region': "CN"}

        return self.post_(address, json=json)
