# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 15:23
# @Author : wangjie
# @File : models.py
# @project : SensoroApi

# 标准库导入
import types
from dataclasses import dataclass
from enum import Enum, unique  # python 3.x版本才能使用
from typing import Text, Dict, Union, Any, Optional, List, Callable
# 第三方库导入
from pydantic import BaseModel


class Environment(Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
    DIANJUN = 'dianjun'




if __name__ == '__main__':
    print(Environment.DEV.name)
    print(Environment.DEV.value)
