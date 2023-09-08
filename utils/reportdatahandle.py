# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/7 16:00
# @Author : wangjie
# @File : report_data_handle.py
# @project : SensoroApi
import json
import os

from configs.dir_path_config import BASE_DIR, PYTEST_RESULT_DIR
from utils.time_utils import TimeUtil


class ReportDataHandle:

    @staticmethod
    # TODO：完善allure报告的统计
    def allure_case_count():
        """统计allure报告收集的case数量"""
        pass

    @staticmethod
    def pytest_json_report_case_count():
        """统计pytest_json_report报告收集的case数量"""
        with open(PYTEST_RESULT_DIR + os.sep + 'pytest_result.json', 'r', encoding='utf-8') as f:
            pytest_result = json.loads(f.read())
            case_count = {}
            case_count["total_case"] = pytest_result['summary'].get("total", 0)  # 用例总数
            case_count["pass_case"] = pytest_result["summary"].get("passed", 0)  # 通过用例数
            case_count["fail_case"] = pytest_result["summary"].get("failed", 0)  # 失败用例数
            case_count["skip_case"] = pytest_result["summary"].get("skipped", 0)  # 跳过用例数
            case_count["xfail_case"] = pytest_result["summary"].get("xfailed", 0)  # 预期失败用例数
            case_count["xpass_case"] = pytest_result["summary"].get("xpassed", 0)  # 预期成功用例数
            case_count["error_case"] = pytest_result["summary"].get("error", 0)  # 报错用例数（比如语法错误导致）
            # 判断运行用例总数大于0
            if case_count["total_case"] > 0:
                # 计算成功率
                case_count["pass_rate"] = round(
                    (case_count["pass_case"] + case_count["xpass_case"]) / case_count["total_case"] * 100, 2)
            else:
                # 如果未运行用例，则成功率为 0.0
                case_count["pass_rate"] = 0.0
            case_count["case_duration"] = round(pytest_result["duration"], 2)  # 用例运行时间
            case_count["case_start_time"] = TimeUtil.unix_time_to_str(int('%.f' % pytest_result["created"]))  # 用例开始时间

            return case_count


if __name__ == '__main__':
    print(ReportDataHandle.pytest_json_report_case_count())
