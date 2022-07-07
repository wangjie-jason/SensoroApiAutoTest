# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi

import pytest
from py.xml import html

from pageApi.login import Login


@pytest.fixture(scope="session", autouse=False)
def get_token():
    """获取登录V1的token"""
    # 获取token前需要先获取验证码
    Login().get_sendSms('13718395478')
    # 调登录接口，获取登录接口的token¬
    login_response = Login().login_v1('13718395478', '111111')
    login_token = login_response.json()['data']['token']
    # 调项目接口，将登录token替换为用户token
    user_response = Login().select_merchant(login_token)
    user_token = user_response.json()['data']['token']
    return user_token


@pytest.fixture(scope="session", autouse=False)
def get_token_v2():
    """获取登录V2的token"""
    # 获取token前需要先获取验证码
    Login().get_sendSms('13718395478')
    # 调登录接口，获取登录接口的token
    login_response = Login().login_v2('13718395478', '111111')
    login_token = login_response.json()['data']['token']
    # 调租户接口，将登录token替换为Avatartoken
    avatar_response = Login().select_tenant(login_token)
    avatar_token = avatar_response.json()['data']['token']
    return avatar_token


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


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    """"pytest-html报告中清除执行成功的用例logs"""
    if report.passed:
        del data[:]
        data.append(html.div('pass用例不展示日志', class_='empty log'))
