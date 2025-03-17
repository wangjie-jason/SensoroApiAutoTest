#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/27 20:57
# @Author : wangjie
# @File : cache_handle.py
# @project : SensoroApiAutoTest
import json

import allure

from common.exceptions import ValueNotFoundError
from utils.allure_handle import allure_attach_text, allure_attach_json

# 定义一个全局变量，用于存储提取的参数内容
_global_data = {}


class CacheHandler:

    @staticmethod
    def set_cache(cache_name, value):
        """
        往全局变量_global_data中存值，用于关联参数
        :return:
        """

        _global_data[cache_name] = value
        with allure.step("设置缓存成功"):
            allure_attach_text("存入缓存", str(f"'{cache_name}':'{value}'"))
            allure_attach_json("当前可使用的缓存", json.dumps(_global_data, ensure_ascii=False, indent=4))

    @staticmethod
    def get_cache(cache_data):
        """
        从全局变量_global_data中取值
        :return:
        """

        try:
            with allure.step("提取缓存成功"):
                allure_attach_text("取出缓存", str(f"{cache_data}:{_global_data.get(cache_data, None)}"))
            return _global_data[cache_data]
        except KeyError:
            with allure.step("提取缓存失败"):
                allure_attach_json("提取缓存失败，当前可使用的缓存",
                                   json.dumps(_global_data, ensure_ascii=False, indent=4))
            raise ValueNotFoundError(f"{cache_data}的缓存数据未找到，请检查是否将该数据存入缓存中")


if __name__ == '__main__':
    CacheHandler.set_cache("a", "1")
    print(CacheHandler.get_cache("a"))