# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi

import pytest

from page_api.login import Login


@pytest.fixture(scope="session", autouse=False)
def get_token():
    """获取登录token"""
    # 获取token前需要先获取验证码
    Login().get_sendSms('13718395478')
    return Login().login('13718395478', '111111')['data']['token']
