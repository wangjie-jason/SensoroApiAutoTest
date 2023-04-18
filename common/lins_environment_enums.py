# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 15:23
# @Author : wangjie
# @File : lins_environment_enums.py
# @project : SensoroApi

from enum import Enum


class Environment(Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
    DIANJUN = 'dianjun'


if __name__ == '__main__':
    print(Environment.DEV.name)
    print(Environment.DEV.value)
