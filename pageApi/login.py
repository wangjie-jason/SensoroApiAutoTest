#!/usr/bin/python
# -*- coding:utf-8 -*-
from common.base_api import BaseApi
from utils.time_utils import TimeUtil


class Login(BaseApi):
    """登录模块"""

    def login(self, username, password):
        """获取登录权限"""
        address = '/user/login'
        json = {
            'username': username,
            'password': password
        }

        return self.send_post_request(address, json_data=json)


if __name__ == '__main__':
    r = Login().login('18800000001', '123456')
