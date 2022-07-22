#!/usr/bin/python
# -*- coding:utf-8 -*-
from common.http_method import BaseApi
from utils.time_utils import TimeUtil


class Login(BaseApi):
    """登录模块"""

    def get_sendSms(self, mobile):
        """获取手机号验证码"""
        address = 'auth/v1/sendSms'
        params = {
            'mobile': mobile,
            'region': 'CN'}

        return self.get_(address, params=params)

    def login_v1(self, mobile, sms_code):
        """登录V1权限"""
        address = 'auth/v1/loginByMobile'
        json = {
            'sessionId': "018pT9kOhM2HyUciiIhkMNQW3X22EydkN2ZSG3_h26UhsRJPOUCUAJfFzae-5_k_cU0Auw03ocNqlFM_dWbIWZE1OCFecobl9BvRfCBJTS1_lypbdxU97CpNssyX9kcqkv",
            'sig': "05XqrtZ0EaFgmmqIQes-s-CAiu5y6YBKaSb9AKSL5UbzpDSilBMvhSwiXdbW4r0pATPpuHcErPtBVQb4T02lxA-qXfhyddfcu1iWhmGu9QsPK57UVcRnFNnulf2Qcn6OK7F4X3BvT9lmcJ1pFVxew7PyNaG1nrqsFKgXWTIfKDE5txdIp6Dpd_xDkUZUaCuDHKFZO3KxUTrusHohfcRFSf3vTfA5EQEfyztOrWkZW-NGoUjgPgQvLzTpWSOm2JCTNmfoCOZltk2IX8EXfWk-56-z0AFHvU-jDkqi0udtdeDrveaNYC7kddMKqCOML4fNgMQwi6wQHVvY6Rh5yNKBcihg",
            'token': "1648286210510:0.5175585315118147",
            'scene': "ic_login",
            'appKey': "FFFF0N00000000008D02",
            'mobile': mobile,
            'smsCode': sms_code,
            'region': "CN"}

        return self.post_(address, json=json)

    def login_v2(self, mobile, sms_code):
        """登录V2权限"""
        address = 'auth/v2/web/loginByMobile'
        json = {
            'sessionId': "0140ZMxqkYxeUxUoDRmE5z6uPBWemi7wYog-qD50OnEDTqLU3OIrq0OdGw4LHeLf7yPk4pWLAc-x7klRRBJRQogjJa4ffJF2wOmKtisFTjST_Ad_IsfE7ZFXTTD9aHfT0Oc7G0oUO3ksNDTjLiXL17Km1bmAqSrr-KWPjaofay5xQ",
            'sig': "05XqrtZ0EaFgmmqIQes-s-CAdbQPsrteVLJ6HcTastLF9-tfS5AFBtjtzYoRJuOSYkOT5Yf9_PpHhoOEVaTuu2MrTnGTj6NI7cpPr7y3eLEzUPzPeQZG-AUw3vjox7Wxb129C6fh_JTmT9VsfDCyl6M8HX-5kDV99p0KcqdPJWUI08alyMRA00xXUqAbAD9RvYUSVjt3rPT3YkWLHwQWq4LgIBCAu6Xi7g4JTrg7ckqqcw0wEIKA__alS2zwFWsP4yCQyYxV6CcCY23E_fQUl-h9cJ374bDzVrtRWXZ7aW2MWFHWbld765kgMI2UYsNXU8IGOjapQNsLh_Mtq5FL3TR0ppZabA02_8q3AWa9Nd1hDfNBEVVGUQPh2kzea2ZLyd007bJdyoAQE0lLtVcAwQaX_fFglQFdDAAloiYYa3wqG5xwvm5YY9QTvwH_8vLv2l",
            'token': "FFFF0N00000000008D02:ic_login:1655731619074:0.22770540477933277",
            'scene': "ic_login",
            'appKey': "FFFF0N00000000008D02",
            'mobile': mobile,
            'smsCode': sms_code,
            'region': "CN",
            'selectedTime': TimeUtil.get_current_time_unix()
        }

        return self.post_(address, json=json)

    def select_merchant(self, token,x_lins_view='all'):
        """选择项目"""
        address = 'auth/v1/selectMerchant'
        headers = {
            'Authorization': f'Bearer {token}',
            'x-lins-view':x_lins_view
        }
        return self.get_(address=address, headers=headers)

    def select_tenant(self, token):
        """切换租户"""
        address = 'auth/v1/tenant/selectTenant'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        return self.get_(address=address, headers=headers)


if __name__ == '__main__':
    Login().select_tenant(
        'eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4Iiwibmlja25hbWUiOiLmsarmnbAiLCJleHAiOjE2NTYzOTc5ODgsImlhdCI6MTY1NTc5MzE4OCwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCIsInJlZnJlc2hUb2tlbiI6IjdkM2Q3ZmJiMGY0YjQxOTE5NDJhNDNjMzg1ODdkZTRjIn0.QhSWRjmDVMLlTkb1cmv5qi8KjWQ37bzahpAxFA8Y_9SGxyQ5q1UHup-RIa3vF_AG5OTPPf_5wjfG75K9GF80Jw')
    Login().get_sendSms('13718395478')