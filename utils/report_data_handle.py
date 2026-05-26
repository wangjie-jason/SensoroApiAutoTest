#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/7 16:00
# @Author : wangjie
# @File : report_data_handle.py
# @project : SensoroApiAutoTest
import json

from core.models import TestMetrics
from core.paths import PYTEST_RESULT_DIR
from utils.time_util import TimeUtil


class ReportDataHandle:

    @staticmethod
    # TODO：完善allure报告的统计
    def allure_case_count():
        """统计allure报告收集的case数量"""
        pass

    @staticmethod
    def pytest_json_report_case_count():
        """统计pytest_json_report报告收集的case数量"""
        with open(PYTEST_RESULT_DIR / 'pytest_result.json', 'r', encoding='utf-8') as f:
            pytest_result = json.load(f)
        case_count = {}
        summary = pytest_result.get("summary", {})
        case_count["total"] = summary.get("total", 0)  # 用例总数
        case_count["passed"] = summary.get("passed", 0)  # 通过用例数
        case_count["failed"] = summary.get("failed", 0)  # 失败用例数
        case_count["rerun"] = summary.get("rerun", 0)  # 重试通过用例数
        case_count["skipped"] = summary.get("skipped", 0)  # 跳过用例数
        case_count["xfailed"] = summary.get("xfailed", 0)  # 预期失败用例数
        case_count["xpassed"] = summary.get("xpassed", 0)  # 预期成功用例数
        case_count["error"] = summary.get("error", 0)  # 报错用例数（比如语法错误导致）
        # 判断运行用例总数大于0
        if case_count["total"] > 0:
            # 计算成功率
            case_count["pass_rate"] = round(
                (case_count["passed"] + case_count["rerun"] + case_count["xpassed"]) / case_count["total"] * 100, 2)
        else:
            # 如果未运行用例，则成功率为 0.0
            case_count["pass_rate"] = 0.0
        case_count["duration"] = round(pytest_result["duration"], 2)  # 用例运行时间
        case_count["start_time"] = TimeUtil.unix_to_str(int('%.f' % pytest_result["created"]))  # 用例开始时间

        return TestMetrics(**case_count)


if __name__ == '__main__':
    print(ReportDataHandle.pytest_json_report_case_count())
