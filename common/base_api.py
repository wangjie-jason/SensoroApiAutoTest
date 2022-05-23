#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests


class BaseApi():
    """基础类，提供公共方法"""

    def send_(self, data):
        """发送请求，返回json格式数据"""
        r = requests.request(**data)
        return r.json()

    def delete_(self):
        """删除请求，返回json格式数据"""
        pass

    def put_(self):
        """修改请求，返回json格式数据"""
        pass
