# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi
import os.path
import platform

import allure
import pytest
from py.xml import html

from common.settings import ENV
from configs.dir_path_config import BASE_DIR


@pytest.fixture(scope="session", autouse=True)
def set_allure_env():
    """设置allure报告的环境变量信息"""
    allure_env = {
        'OperatingEnvironment': ENV.name,
        'Python': platform.python_version(),
        'Platform': platform.platform(),
        'Pytest': pytest.__version__,
    }
    allure_env_file = os.path.join(BASE_DIR, 'environment.properties')
    with open(allure_env_file, 'w', encoding='utf-8') as f:
        for _k, _v in allure_env.items():
            f.write(f'{_k}={_v}\n')
    # with open(allure_env_file, 'r', encoding='utf-8') as f:
    #     allure.attach(f.read(), '环境信息', allure.attachment_type.TEXT)


def pytest_configure(config):
    """修改pytest-html报告中Environment项目展示的信息"""
    # 添加项目名称
    config._metadata["项目名称"] = "lins接口自动化测试"
    # 删除Java_Home
    config._metadata.pop("JAVA_HOME")
    # 删除Plugins
    config._metadata.pop("Plugins")


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    """修改pytest-html报告中添加summary内容"""
    prefix.extend([html.p("所属部门: 测试组")])
    prefix.extend([html.p("测试人员: 汪杰")])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    """pytest-html报告中表头添加Description"""
    cells.insert(1, html.th('Description'))  # 表头添加Description
    cells.pop(-1)  # 删除link


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """修改pytest-html报告中表头Description对应的内容为测试用例的描述"""
    cells.insert(1, html.td(report.description))  # 表头对应的内容
    cells.pop(-1)  # 删除link列


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):  # description取值为用例说明__doc__
    """修改pytest-html报告中description取值为用例说明__doc__"""
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


# @pytest.mark.optionalhook
# def pytest_html_results_table_html(report, data):
#     """"pytest-html报告中清除执行成功的用例logs"""
#     if report.passed:
#         del data[:]
#         data.append(html.div('pass用例不展示日志', class_='empty log'))
