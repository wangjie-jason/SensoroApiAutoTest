# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 15:23
# @Author : wangjie
# @File : lins_environment_enum.py
# @project : SensoroApi

from enum import Enum


class Environment(Enum):
    DEV = 0
    TEST = 1
    PROD = 2
    DIANJUN = 3
