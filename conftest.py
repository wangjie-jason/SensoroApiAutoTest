# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi

import pytest
from py.xml import html

from common.http_method import BaseApi
from pageApi.login import Login

# 定义一个全局变量，用于存储提取的参数内容
global_data = {}


@pytest.fixture(scope="session", autouse=False)
def set_global_data():
    """
    设置全局变量，用于关联参数
    :return:
    """

    def _set_global_data(key, value):
        global_data[key] = value
        print('当前可使用的全局变量：', global_data)

    yield _set_global_data
    global_data.clear()


@pytest.fixture(scope="session", autouse=False)
def get_global_data():
    """
    从全局变量global_data中取值
    :return:
    """

    def _get_global_data(key):
        return global_data.get(key)

    return _get_global_data


@pytest.fixture(scope="session", autouse=False)
def get_token():
    """获取登录V1的token"""
    # 登录前需要先获取验证码
    Login().get_sendSms('13800000000')
    # 调登录接口，获取登录接口的token¬
    login_response = Login().login_v1('13800000000', '138000')
    token = BaseApi.get_json(login_response)['data']['token']
    return token


@pytest.fixture(scope="session", autouse=False)
def get_token_v2():
    """获取登录V2的Ai视频管理项目的token"""
    # 登录前需要先获取验证码
    Login().get_sendSms('13800000000')
    # 调登录接口，获取登录接口的token
    login_response = Login().login_app_v2('13800000000', '138000')
    login_token = BaseApi.get_json(login_response)['data']['token']
    # 调切换租户的接口，获取切换到指定租户的token
    headers = {'Authorization': f'Bearer {login_token}'}
    res = Login().select_tenant(tenantId='1622903542623612930', projectId='1622903550156582913', headers=headers)
    token = BaseApi.get_json(res)['data']['token']
    return token


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
