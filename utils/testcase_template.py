# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/7/7 11:47
# @Author : wangjie
# @File : testcase_template.py
# @project : SensoroApi

f = """
import pytest
from loguru import logger
import allure
from case_utils.assert_handle import assert_response, assert_sql
from case_utils.request_data_handle import RequestPreDataHandle, RequestHandle, after_request_extract
from case_utils.allure_handle import allure_title
from config.settings import db_info
from config.global_vars import GLOBAL_VARS
from pytest_html import extras  # 往pytest-html报告中填写额外的内容



@allure.epic("${allure_epic}")
@allure.feature("${allure_feature}")
class ${class_title}Auto:

    @allure.story("${allure_story}")
    @pytest.mark.auto
    @pytest.mark.parametrize("case", cases, ids=["{}".format(case["title"]) for case in cases])
    def ${func_title}_auto(self, case, extra):
        # 添加用例标题作为allure中显示的用例标题
        allure_title(case.get("title", ""))
        # 处理请求前的用例数据
        case_data = RequestPreDataHandle(case).request_data_handle()
        # 将用例数据显示在pytest-html报告中
        extra.append(extras.text(str(case_data), name="用例数据"))
        # 发送请求
        response = RequestHandle(case_data).http_request()
        # 将响应数据显示在pytest-html报告中
        extra.append(extras.text(str(response.text), name="响应数据"))
        # 进行响应断言
        assert_response(response, case_data["assert_response"])
        # 进行数据库断言
        assert_sql(db_info[GLOBAL_VARS["env_key"]], case_data["assert_sql"])
        # 断言成功后进行参数提取
        after_request_extract(response, case_data.get("extract", None))
"""
