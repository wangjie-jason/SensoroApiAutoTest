#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApiAutoTest
import time

import pytest

from utils.report_data_handle import ReportDataHandle


def pytest_sessionstart():
    """在整个pytest运行过程开始之前执行的操作"""
    pass


def pytest_sessionfinish(session, exitstatus):
    """在整个pytest session结束后执行的操作"""
    pass


def pytest_collection_modifyitems(items) -> None:
    """解决控制台用例参数化中文编码问题"""
    # 会使pytest-html报告里面的中文乱码，需要去手动改一下pytest-html源码即可
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


def pytest_configure(config):
    """修改pytest-html报告中Environment项目展示的信息"""
    pass


def pytest_metadata(metadata: dict):
    """修改pytest的metadata数据，在pytest-html报告中体现在Environment展示的信息"""
    # 添加项目名称
    metadata['项目名称'] = 'lins接口自动化测试'
    # 删除Java_Home信息
    metadata.pop("JAVA_HOME")
    # 删除Plugins
    # metadata.pop("Plugins")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_summary(prefix):
    """修改pytest-html报告中添加summary内容"""
    prefix.extend(["<p>所属部门: 测试组</p>"])
    prefix.extend(["<p>测试人员: 汪杰</p>"])


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    """pytest-html报告中表头添加Description"""
    cells.insert(1, "<th>Description</th>")  # 表头添加Description
    cells.pop(-1)  # 删除link


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    """修改pytest-html报告中表头Description对应的内容为测试用例的描述"""
    cells.insert(1, f"<td>{report.description}</td>")  # 表头对应的内容
    cells.pop(-1)  # 删除link列


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # description取值为用例说明__doc__
    """获取测试结果、生成测试报告"""
    outcome = yield
    report = outcome.get_result()
    # 修改报告中description取值为用例说明__doc__
    report.description = str(item.function.__doc__)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集测试结果展示在控制台"""
    pytest_result = ReportDataHandle.pytest_json_report_case_count()
    run_time = round((time.time() - terminalreporter._sessionstarttime), 2)
    print("******用例执行结果统计******")
    print(f"总用例数：{pytest_result.total}条")
    print(f"通过：{pytest_result.passed}条")
    print(f"重试后通过：{pytest_result.rerun}条")
    print(f"失败：{pytest_result.failed}条")
    print(f"跳过：{pytest_result.skipped}条")
    print(f"预期失败：{pytest_result.xfailed}条")
    print(f"预期通过：{pytest_result.xpassed}条")
    print(f"报错：{pytest_result.error}条")
    print(f"用例通过率：{pytest_result.pass_rate}%")
    print(f"用例开始时间：{pytest_result.start_time}")
    print(f"用例执行时间：{pytest_result.duration}s")
    print(f"总用时(算上了生成报告的时间)：{run_time}s")
