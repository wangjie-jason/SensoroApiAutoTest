# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/10 18:27
# @Author : wangjie
# @File : lock_reset.py
# @project : SensoroApi
from common.http_method import BaseApi
from pageApi.login import Login


def get_token():
    """获取登录SCOM_V1的token"""
    # 获取token前需要先获取验证码
    phone = input('请输入你的手机号：')
    Login().get_sendSms(phone)
    # 调登录接口，获取登录接口的token
    login_response = Login().login_scom_v1(phone, input('请输入验证码：'))
    login_token = login_response.json()['data']['token']
    # 调项目接口，将登录token替换为用户token
    params = {'merchantId': 0}
    headers = {
        'Authorization': f'Bearer {login_token}',
        'x-lins-view': 'default'
    }
    user_response = Login().select_merchant(params=params, headers=headers)
    user_token = user_response.json()['data']['token']
    return user_token


def lock_reset():
    """门禁出厂，需要去configs/lins_environment.ini文件下修改至对应环境的host"""
    address = '/enter/v1/enter/release'
    data = {
        'version': 'OA',
        'prefix': 'Test1-',
        # 生产环境：'productId': 'c14397fe-1462-11ec-a2de-0e0d1d54f276'
        # 点军环境：'productId': '26aa8aa7-d266-11ec-be12-ee7960eede4b'
        # 测试环境：'productId': '609594a2-f4fd-11eb-98f1-363f1ff6b505'
        # 开发环境：'productId': '3347b3b7-cda4-11eb-b0ab-9a27cf714ac0'
        'productId': '26aa8aa7-d266-11ec-be12-ee7960eede4b',
    }
    files = [
        ('file', ('门禁出厂.xlsx', open('/Users/wangjie/Desktop/门禁出厂.xlsx', 'rb'),
                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    ]
    headers = {
        # 用0号商户的token
        'Authorization': f'Bearer {get_token()}'
    }
    return BaseApi().post(address, data=data, files=files, headers=headers)


if __name__ == '__main__':
    lock_reset()
