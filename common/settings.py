# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:45
# @Author : wangjie
# @File : settings.py
# @project : SensoroApi

from configs.lins_environment_enum import Environment

# 设置运行的环境变量
env = Environment.TEST

# 设置是否需要发送邮件：Ture发送，False不发送
IS_SEND = False