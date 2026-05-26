#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/27 20:31
# @Author : wangjie
# @File : cache_util.py
# @project : SensoroApiAutoTest
"""测试用例间数据共享缓存，基于 fixture 机制，避免全局可变状态"""
import json

import allure

from core.exceptions import ValueNotFoundError
from utils.allure_util import allure_attach_text, allure_attach_json


class CacheUtil:
    """缓存管理器，通过 fixture 注入的字典实例进行数据共享"""

    def __init__(self, storage: dict = None):
        self._storage = storage if storage is not None else {}

    def set(self, name: str, value):
        """存入缓存"""
        self._storage[name] = value
        with allure.step("设置缓存成功"):
            allure_attach_text("存入缓存", f"'{name}': '{value}'")
            allure_attach_json("当前可使用的缓存",
                               json.dumps(self._storage, ensure_ascii=False, indent=4))

    def get(self, name: str):
        """取出缓存，不存在时抛出 ValueNotFoundError"""
        try:
            value = self._storage[name]
            with allure.step("提取缓存成功"):
                allure_attach_text("取出缓存", f"{name}: {value}")
            return value
        except KeyError:
            with allure.step("提取缓存失败"):
                allure_attach_json("当前可使用的缓存",
                                   json.dumps(self._storage, ensure_ascii=False, indent=4))
            raise ValueNotFoundError(f"缓存数据 '{name}' 未找到，请检查是否已存入缓存")


if __name__ == '__main__':
    ca = CacheUtil()
    ca.set('a', 1)
    print(ca.get('a'))
