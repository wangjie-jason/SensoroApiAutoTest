# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/1 20:47
# @Author : wangjie
# @File : dir_path_config.py
# @project : SensoroApi

import os

# 当前项目的根路径
BASE_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

# common目录的路径
COMMON_DIR = os.path.join(BASE_DIR, 'common')

# configs目录的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# datas目录的路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# files目录的路径
FILES_DIR = os.path.join(BASE_DIR, 'files')

# pageApi目录的路径
PAGE_API_DIR = os.path.join(BASE_DIR, 'pageApi')

# testCase目录的路径
TEST_CASE_DIR = os.path.join(BASE_DIR, 'testCase')

# utils目录的路径
UTILS_DIR = os.path.join(BASE_DIR, 'utils')

# outFiles目录的路径
OUT_FILES_DIR = os.path.join(BASE_DIR, 'outFiles')

# logs目录的路径
LOGS_DIR = os.path.join(OUT_FILES_DIR, 'logs')

# pytest_report目录的路径
PYTEST_REPORT_DIR = os.path.join(OUT_FILES_DIR, 'pytest_report')

# pytest_result目录的路径
PYTEST_RESULT_DIR = os.path.join(OUT_FILES_DIR, 'pytest_result')

# allure_report目录的路径
ALLURE_REPORT_DIR = os.path.join(OUT_FILES_DIR, 'allure_report')

# screeShot目录的路径
SCREENSHOT_DIR = os.path.join(OUT_FILES_DIR, 'screeShot')

# Temp目录的路径
TEMP_DIR = os.path.join(OUT_FILES_DIR, 'Temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
