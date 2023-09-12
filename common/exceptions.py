# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/7 17:33
# @Author : wangjie
# @File : exceptions.py.py
# @project : SensoroApi

"""自定义报错"""


class MyBaseFailure(Exception):
    pass


class JsonpathExtractionFailed(MyBaseFailure):
    pass


class NotFoundError(MyBaseFailure):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class SqlNotFound(NotFoundError):
    pass


class AssertTypeError(MyBaseFailure):
    pass


class DataAcquisitionFailed(MyBaseFailure):
    pass


class ValueTypeError(MyBaseFailure):
    pass


class SendMessageError(MyBaseFailure):
    pass


class ValueNotFoundError(MyBaseFailure):
    pass


class DataProcessorFuncError(MyBaseFailure):
    pass
