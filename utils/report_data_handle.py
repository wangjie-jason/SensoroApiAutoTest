#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/7 16:00
# @Author : wangjie
# @File : report_data_handle.py
# @project : SensoroApiAutoTest
import json

from core.logger import logger
from core.models import TestMetrics
from core.paths import PYTEST_RESULT_DIR
from utils.time_util import TimeUtil


class ReportDataHandle:
    """报告数据处理工具类"""

    @staticmethod
    # TODO：完善allure报告的统计
    def allure_case_count() -> None:
        """统计 allure 报告收集的 case 数量（待实现）"""
        pass

    @staticmethod
    def pytest_json_report_case_count() -> TestMetrics:
        """
        解析 pytest-json-report 生成的 JSON 结果文件，统计用例执行数据并返回 TestMetrics

        数据来源于 pytest-json-report 插件的 summary 字段，包含：
        - total / passed / failed / rerun / skipped / xfailed / xpassed / error：各类用例计数
        - pass_rate：通过率（%），计算公式为 (passed + rerun + xpassed) / total * 100
        - duration：总运行时长（秒）
        - start_time：用例开始时间（格式化字符串）

        :return: 包含完整统计指标的 TestMetrics 对象，文件不存在或解析失败时返回 None
        """
        json_path = PYTEST_RESULT_DIR / 'pytest_result.json'

        # 读取 pytest JSON 结果文件
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                pytest_result: dict = json.load(f)
        except FileNotFoundError:
            logger.error(f"pytest 结果文件不存在: {json_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"pytest 结果文件 JSON 解析失败: {json_path}，错误: {e}")
            return None

        # 提取 summary 字段，各计数项默认值为 0
        summary: dict = pytest_result.get("summary", {})

        total = summary.get("total", 0)  # 用例总数
        passed = summary.get("passed", 0)  # 通过用例数
        failed = summary.get("failed", 0)  # 失败用例数
        rerun = summary.get("rerun", 0)  # 重试通过用例数
        skipped = summary.get("skipped", 0)  # 跳过用例数
        xfailed = summary.get("xfailed", 0)  # 预期失败用例数
        xpassed = summary.get("xpassed", 0)  # 预期成功用例数
        error = summary.get("error", 0)  # 报错用例数（如语法错误导致）

        # 计算通过率：通过 + 重试通过 + 预期成功 / 总数
        if total > 0:
            pass_rate = round((passed + rerun + xpassed) / total * 100, 2)
        else:
            pass_rate = 0.0

        # 运行时长（秒），取小数点后两位
        duration = round(pytest_result.get("duration", 0), 2)

        # 开始时间：pytest created 为秒级浮点时间戳，转为可读字符串
        created = pytest_result.get("created", 0)
        start_time = TimeUtil.unix_to_str(int(created))

        return TestMetrics(
            total=total,
            passed=passed,
            failed=failed,
            rerun=rerun,
            skipped=skipped,
            xfailed=xfailed,
            xpassed=xpassed,
            error=error,
            pass_rate=pass_rate,
            start_time=start_time,
            duration=duration,
        )


if __name__ == '__main__':
    result = ReportDataHandle.pytest_json_report_case_count()
    print(result)
