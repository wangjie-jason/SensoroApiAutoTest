# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi
import os.path
import platform
import shutil

import pytest
from py.xml import html

from common.settings import ENV
from configs.dir_path_config import BASE_DIR
from configs.lins_environment import EntryPoint


def pytest_sessionstart():
    """在整个pytest运行过程开始之前设置allure报告的环境变量信息"""
    allure_env = {
        'OperatingEnvironment': ENV.name,
        'BaseUrl': EntryPoint.URL(),
        'PythonVersion': platform.python_version(),
        'Platform': platform.platform(),
        'PytestVersion': pytest.__version__,
    }
    allure_env_file = os.path.join(BASE_DIR, 'environment.properties')
    with open(allure_env_file, 'w', encoding='utf-8') as f:
        for _k, _v in allure_env.items():
            f.write(f'{_k}={_v}\n')


def pytest_sessionfinish(session, exitstatus):
    """运行完成后生成allure报告文件，再将本地启动方式放入该目录下"""
    # allure报告展示environment时所需要的数据，这里是在项目根路径下创建的environment.properties文件拷贝到allure-report报告中,保证环境文件不会被清空
    shutil.copy('./environment.properties', './Temp/environment.properties')
    # allure报告展示运行器时所需要的数据
    shutil.copy('./executor.json', './Temp/executor.json')
    # 使用allure generate -o 命令将./Temp目录下的临时报告导出到TestReport目录
    os.system('allure generate ./Temp -o ./outFiles/report --clean')
    # 将本地启动脚本和查看allure报告方法放入报告目录下面
    shutil.copy('./open_report.sh', './outFiles/report/open_report.sh')
    shutil.copy('./查看allure报告方法', './outFiles/report/查看allure报告方法')


def pytest_collection_modifyitems(items) -> None:
    """解决控制台用例参数化中文编码问题"""
    # 会使pytest-html报告里面的中文乱码，需要去手动改一下pytest-html源码即可
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


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
