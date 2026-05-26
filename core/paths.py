#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/1 20:47
# @Author : wangjie
# @File : paths.py
# @project : SensoroApiAutoTest

from pathlib import Path

# 当前项目的根路径
BASE_DIR = Path(__file__).resolve().parents[1]

# core目录的路径
CORE_DIR = BASE_DIR / 'core'

# config目录的路径
CONFIG_DIR = BASE_DIR / 'config'

# data目录的路径
DATAS_DIR = BASE_DIR / 'data'

# files目录的路径
FILES_DIR = BASE_DIR / 'files'

# apis目录的路径
APIS_DIR = BASE_DIR / 'apis'

# testcase目录的路径
TESTCASE_DIR = BASE_DIR / 'testcase'

# utils目录的路径
UTILS_DIR = BASE_DIR / 'utils'

# output目录的路径
OUTPUT_DIR = BASE_DIR / 'output'

# logs目录的路径
LOGS_DIR = OUTPUT_DIR / 'logs'

# pytest_report目录的路径
PYTEST_REPORT_DIR = OUTPUT_DIR / 'pytest_report'

# pytest_result目录的路径
PYTEST_RESULT_DIR = OUTPUT_DIR / 'pytest_result'

# allure_report目录的路径
ALLURE_REPORT_DIR = OUTPUT_DIR / 'allure_report'

# allure_result目录的路径
ALLURE_RESULT = OUTPUT_DIR / 'allure_result'

# screenshot目录的路径
SCREENSHOT_DIR = OUTPUT_DIR / 'screenshot'

# 目录不存在时自动创建
ALLURE_RESULT.mkdir(exist_ok=True, parents=True)
