# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/8 19:13
# @Author : wangjie
# @File : jenkins_handle.py
# @project : SensoroApiAutoTest
import os


def get_env_from_jenkins(name, base=''):
    """从Jenkins中获取全局环境变量"""
    return os.getenv(name) and os.getenv(name).strip() or base


ProjectName = get_env_from_jenkins("JOB_NAME")  # Jenkins构建项目名称
BUILD_URL = get_env_from_jenkins("BUILD_URL")  # Jenkins构建项目URL
BUILD_NUMBER = get_env_from_jenkins("BUILD_NUMBER")  # Jenkins构建编号
ALLURE_URL = BUILD_URL + 'allure/'  # Jenkins构建的allure报告地址
