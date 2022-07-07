# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/1 20:47
# @Author : wangjie
# @File : dir_path_config.py
# @project : SensoroApi

import os

# 当前项目的路径
BASE_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
# common目录的路径
COMMON_DIR = os.path.join(BASE_DIR, 'common')
# configs目录的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')
# datas目录的路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')
# pageApi目录的路径
PAGE_API_DIR = os.path.join(BASE_DIR, 'pageApi')
# testCase目录的路径
TEST_CASE_DIR = os.path.join(BASE_DIR, 'testCase')
# utils目录的路径
UTILS_DIR = os.path.join(BASE_DIR, 'utils')
