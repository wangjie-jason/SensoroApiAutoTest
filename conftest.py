# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi
import os.path
import platform
import shutil
import time

import pytest

from common.settings import ENV
from configs.dir_path_config import BASE_DIR
from configs.lins_environment import EntryPoint
from utils.reportdatahandle import ReportDataHandle


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
    # # allure报告展示environment时所需要的数据，这里是在项目根路径下创建的environment.properties文件拷贝到allure-report报告中,保证环境文件不会被清空
    # FileHandle.copy_file(BASE_DIR + os.sep + 'environment.properties', TEMP_DIR)
    # # allure报告展示运行器时所需要的数据
    # FileHandle.copy_file(BASE_DIR + os.sep + 'executor.json', TEMP_DIR)
    # # 使用allure generate -o 命令将./Temp目录下的临时报告生成到Report目录下变成html报告
    # os.system(f'allure generate {TEMP_DIR} -o {ALLURE_REPORT_DIR} --clean')
    # # 将本地启动脚本和查看allure报告方法放入报告目录下面
    # FileHandle.copy_file(BASE_DIR + os.sep + 'open_report.sh', ALLURE_REPORT_DIR)
    # FileHandle.copy_file(BASE_DIR + os.sep + '查看allure报告方法', ALLURE_REPORT_DIR)


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
    print(f"总用例数：{pytest_result['total_case']}条")
    print(f"通过：{pytest_result['pass_case']}条")
    print(f"失败：{pytest_result['fail_case']}条")
    print(f"跳过：{pytest_result['skip_case']}条")
    print(f"预期失败：{pytest_result['xfail_case']}条")
    print(f"预期通过：{pytest_result['xpass_case']}条")
    print(f"报错：{pytest_result['error_case']}条")
    print(f"用例通过率：{pytest_result['pass_rate']}%")
    print(f"用例执行时间：{pytest_result['case_duration']}s")
    print(f"总用时(算上了生成报告的时间)：{run_time}s")
