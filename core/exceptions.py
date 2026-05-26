#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/7 17:33
# @Author : wangjie
# @File : exceptions.py
# @project : SensoroApiAutoTest

"""自定义报错"""


class MyBaseFailure(Exception):
    """基础异常类"""


class ValueTypeError(MyBaseFailure):
    """值类型错误"""


class SendMessageError(MyBaseFailure):
    """发送消息失败"""


class ValueNotFoundError(MyBaseFailure):
    """缓存值未找到"""


class DataProcessorError(MyBaseFailure):
    """数据处理器错误"""

class ConfigError(MyBaseFailure):
    """配置缺失或非法时抛出。"""
