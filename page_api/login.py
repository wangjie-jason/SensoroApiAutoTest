#!/usr/bin/python
# -*- coding:utf-8 -*-
from common.base_api import BaseApi


class Login(BaseApi):
    """登录模块"""

    def get_sendSms(self, data):
        """获取手机号验证码"""
        return self.send_(data)

    def login(self, data):
        """登录"""
        return self.send_(data)['message']

    def get_token(self,data):
        """获取登录token"""
        return self.send_(data)['data']['token']
