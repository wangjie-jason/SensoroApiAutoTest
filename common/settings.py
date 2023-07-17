# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:45
# @Author : wangjie
# @File : settings.py
# @project : SensoroApi

from common.models import Environment

# 设置运行的环境变量
ENV = Environment.TEST

# 设置是否需要发送邮件：Ture发送，False不发送
IS_SEND_EMAIL = False

# 设置是否需要发送企业微信消息：Ture发送，False不发送
IS_SEND_WECHAT = False

# 设置是否开启debug日志
LOG_DEBUG = False
