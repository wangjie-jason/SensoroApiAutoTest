# !/usr/bin/python
# -*- coding:utf-8 -*-
import json

import requests


class BaseApi:
    """基础类，提供公共方法"""

    def send_(self, data) -> json:
        """发送请求，返回json格式数据"""
        r = requests.request(**data)
        return r.json()

    def delete_(self) -> json:
        """删除请求，返回json格式数据"""
        pass

    def put_(self) -> json:
        """修改请求，返回json格式数据"""
        pass
