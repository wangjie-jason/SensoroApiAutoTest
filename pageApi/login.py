#!/usr/bin/python
# -*- coding:utf-8 -*-
from common.http_method import BaseApi
from utils.time_utils import TimeUtil


class Login(BaseApi):
    """登录模块"""

    def get_sendSms(self, phone):
        """获取手机号验证码"""
        address = '/auth/v2/session/sendSms'
        json = {
            'mobile': phone,
            'region': 'CN'}

        return self.post(address, json=json)

    def login_v1(self, phone, sms_code):
        """登录V1权限"""
        address = '/auth/v1/session/web/loginByMobile'
        json = {
            'captcha': {
                'sessionId': "018pT9kOhM2HyUciiIhkMNQW3X22EydkN2ZSG3_h26UhsRJPOUCUAJfFzae-5_k_cU0Auw03ocNqlFM_dWbIWZE1OCFecobl9BvRfCBJTS1_lypbdxU97CpNssyX9kcqkv",
                'sig': "05XqrtZ0EaFgmmqIQes-s-CAiu5y6YBKaSb9AKSL5UbzpDSilBMvhSwiXdbW4r0pATPpuHcErPtBVQb4T02lxA-qXfhyddfcu1iWhmGu9QsPK57UVcRnFNnulf2Qcn6OK7F4X3BvT9lmcJ1pFVxew7PyNaG1nrqsFKgXWTIfKDE5txdIp6Dpd_xDkUZUaCuDHKFZO3KxUTrusHohfcRFSf3vTfA5EQEfyztOrWkZW-NGoUjgPgQvLzTpWSOm2JCTNmfoCOZltk2IX8EXfWk-56-z0AFHvU-jDkqi0udtdeDrveaNYC7kddMKqCOML4fNgMQwi6wQHVvY6Rh5yNKBcihg",
                'token': "1648286210510:0.5175585315118147",
                'scene': "ic_login",
                'appKey': "FFFF0N00000000008D02",
                'region': "CN"
            },
            'mobile': phone,
            'smsCode': sms_code,
        }

        return self.post(address, json=json)

    def login_web_v2(self, phone, sms_code):
        """web端登录V2权限"""
        address = '/auth/v2/session/web/loginByMobile'
        json = {
            'captcha': {
                'sessionId': "01uh69nEbJA4gnC1yiS5LNOePBWemi7wYog-qD50OnEDRPgh15wKaVtlJFxynu2MQ3xcbKGBE9ETqkqRJRNcIhokCZDw5Epmxq9IavDJIbvWScEjAMjGLU-fLJtRgL6m-VZjKCQ55yX5tnEwClRn43Pu68Ae4vHV-mvtMNo6yB768",
                'sig': "05XqrtZ0EaFgmmqIQes-s-CMKqsFLZV4Kyd9lFv6g9Sgt-tfS5AFBtjtzYoRJuOSYkm6Z7wQCPrGmFcYCGyzJqZ-XYuSVrP7gQWLU6T2tpcCuZnq4fncMoAXKWPZd64BGjvIkIZsyAoneufO3aMsQdv_pPv2O0x52gkNT9WS_3_E0L_AY66A8qsXDss-DDKYFm72MctAPfu4kGdBYIrLSPbWhm53nVYpzyRBrqyN40jhHMZRmFWpNRPwf3ZQjoK4XodkOR7gDrCPvjD36DJ_rqhyWPn9O15IjRj-SjZHp09qiiDeB0AxkQEe80Y9RyqFMndLcIrrhujfbYeVs-8ECS7eWFotqw0Y0CCaS9ARENgkNiCn4eLRQxIJUtrv1VpvEH-7W8vF3bjBUdKd00qQ4gE9fXHKp5rhMqxXfRQUZwCRLFBX5nnPSJr_SZObpnuKhh",
                'token': "FFFF0N00000000008D02:ic_login:1680516798935:0.3117205915302812",
                'scene': "ic_login",
                'appKey': "FFFF0N00000000008D02",
            },
            'mobile': phone,
            'smsCode': sms_code,
            'region': "CN",
            'selectedTime': TimeUtil.get_current_time_unix()
        }

        return self.post(address, json=json)

    def login_app_v2(self, phone, sms_code):
        """移动端登录V2权限"""
        address = '/auth/v2/session/app/loginByMobile'
        json = {
            'mobile': phone,
            'smsCode': sms_code,
        }

        return self.post(address, json=json)

    def select_tenant(self, tenantId, projectId, headers=None):
        """切换租户/项目"""
        address = '/auth/v2/session/select'
        headers = headers
        json = {
            "tenantId": tenantId,
            "projectId": projectId
        }
        return self.post(address=address, headers=headers, json=json)


if __name__ == '__main__':
    # Login().get_sendSms('13800000000')
    # print(BaseApi.get_json(Login().login_app_v2('13800000000', '138000'))['data']['token'])
    r = Login().select_tenant('1622903542623612930', '1622903550156582913')
    print(BaseApi.request_to_curl(r))
