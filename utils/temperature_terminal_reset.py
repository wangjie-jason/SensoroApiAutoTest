# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/13 16:52
# @Author : wangjie
# @File : temperature_terminal_reset.py
# @project : SensoroApi
from common.http_method import BaseApi
from pageApi.login import Login


def get_token():
    """获取登录V1的token"""
    # 获取token前需要先获取验证码
    mobile = input('请输入你的手机号：')
    Login().get_sendSms(mobile)
    # 调登录接口，获取登录接口的token
    login_response = Login().login_v1(mobile, input('请输入验证码：'))
    login_token = login_response.json()['data']['token']
    # 调项目接口，将登录token替换为用户token
    user_response = Login().select_merchant(login_token, x_lins_view='default')
    user_token = user_response.json()['data']['token']
    return user_token


def temperature_terminal_reset():
    """测温终端出厂，需要去configs/lins_environment.ini文件下修改至对应环境的host"""
    address = 'antiepidemic/v1/antiepidemic/terminal/maker'
    data = {
        'version': 'OA',
        'prefix': '测温终端',
        # 点军环境：'productId': 'bf9e0e0d-d266-11ec-be12-ee7960eede4b'
        # 生产环境：'productId': '493107a6-c168-11ec-8fd3-9eb565365869'
        # 测试环境：'productId': 'd8d151b9-bb9d-11ec-a9ee-fa2020198fdd'
        'productId': 'bf9e0e0d-d266-11ec-be12-ee7960eede4b',  # 需要去物联网中台换相应环境的ID
    }
    files = [
        ('file', ('测温终端出厂.xlsx', open('/Users/wangjie/Desktop/测温终端出厂.xlsx', 'rb'),
                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    ]
    headers = {
        # 用0号商户的token
        'Authorization': f'Bearer {get_token()}'
    }
    return BaseApi().post(address, data=data, files=files, headers=headers)


if __name__ == '__main__':
    temperature_terminal_reset()
