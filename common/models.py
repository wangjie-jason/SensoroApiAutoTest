# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 15:23
# @Author : wangjie
# @File : models.py
# @project : SensoroApi
from dataclasses import dataclass
from enum import Enum
from typing import Text


class Environment(Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
    DIANJUN = 'dianjun'


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    total: int
    passed: int
    failed: int
    skipped: int
    xfailed: int
    xpassed: int
    error: int
    pass_rate: float
    start_time: Text
    duration: float


if __name__ == '__main__':
    print(Environment.DEV.name)
    print(Environment.DEV.value)
