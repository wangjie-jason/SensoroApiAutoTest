#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/26 19:02
# @Author : wangjie
# @File : allure_util.py
# @project : SensoroApiAutoTest
import json
import os
import platform

import allure
import pytest
from requests.structures import CaseInsensitiveDict

from core.models import AllureAttachmentType
from core.paths import ALLURE_RESULT, ALLURE_REPORT_DIR


def allure_title(title: str) -> None:
    """allure中动态生成用例标题"""
    allure.dynamic.title(title)


def allure_attach_text(name: str, body: str = None) -> None:
    """
    allure报告添加文本格式附件
    :param name: 附件名称
    :param body: 附件内容
    :return:
    """
    if body is None:
        body = "None"
    elif not isinstance(body, str):
        body = str(body)
    allure.attach(body=body, name=name, attachment_type=allure.attachment_type.TEXT)


def allure_attach_json(name: str, body: str | dict | CaseInsensitiveDict | None = None) -> None:
    """
    allure报告添加json格式附件
    :param name: 附件名称
    :param body: 附件内容
    :return:
    """
    if isinstance(body, CaseInsensitiveDict):
        body = dict(body)
    try:
        if isinstance(body, dict):
            body = json.dumps(body, ensure_ascii=False, indent=4)
        elif body is None:
            body = "None"
        elif isinstance(body, str):
            body = json.dumps(json.loads(body), indent=4, ensure_ascii=False)
        else:
            body = body
    except (json.JSONDecodeError, TypeError):
        body = body
    allure.attach(body=body, name=name, attachment_type=allure.attachment_type.JSON)


def allure_attach_file(name: str, source: str):
    """
    allure报告上传附件、图片、excel等
    :param name: 名称
    :param source: 文件路径，相当于传一个文件
    :return:
    """
    if not os.path.isfile(source):
        raise f"文件不存在: {source}"
    _name = source.split('.')[-1].lower()
    attachment_type_mapping = {enum.value.lower(): getattr(allure.attachment_type, enum.name.upper())
                               for enum in AllureAttachmentType}
    _attachment_type = attachment_type_mapping.get(_name, None)
    try:
        allure.attach.file(
            source=source,
            name=name,
            attachment_type=_attachment_type,
            extension=_name
        )
    except Exception as e:
        raise f"上传文件 {source} 时出错: {e}"


class AllureReportBeautiful:
    """
    美化allure测试报告
    """

    @staticmethod
    def set_windows_title(new_title):
        """
        设置打开的 Allure 报告的浏览器窗口标题文案
        @param new_title:  需要更改的标题文案 【 原文案为：Allure Report 】
        @return:
        """
        report_title_filepath = ALLURE_REPORT_DIR / "index.html"
        with open(report_title_filepath, 'r+', encoding="utf-8") as f:
            all_the_lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in all_the_lines:
                f.write(line.replace("Allure Report", new_title))
            f.close()

    @staticmethod
    def set_report_name(new_name):
        """
        修改Allure报告Overview的标题文案
        @param new_name:  需要更改的标题文案 【 原文案为：ALLURE REPORT 】
        @return:
        """
        title_filepath = os.path.join(ALLURE_REPORT_DIR, "widgets", "summary.json")
        if not os.path.exists(title_filepath):
            raise FileNotFoundError(f"修改报告名称时，summary.json文件未找到： {title_filepath}")
        with open(title_filepath, 'r', encoding='utf-8') as f:
            params = json.load(f)
        params['reportName'] = new_name
        with open(title_filepath, 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False, indent=4)

    @staticmethod
    def set_report_env_on_results():
        """
        在allure-results报告的根目录下生成一个写入了环境信息的文件：environment.properties(注意：不能放置中文，否则会出现乱码)
        @return:
        """
        from core.config_manager import config
        allure_env = {
            'OperatingEnvironment': config.current_env(),
            'BaseUrl': config.base_url(),
            'PythonVersion': platform.python_version(),
            'Platform': platform.platform(),
            'PytestVersion': pytest.__version__,
        }
        allure_env_file = ALLURE_RESULT / 'environment.properties'
        with open(allure_env_file, 'w', encoding='utf-8') as f:
            for _k, _v in allure_env.items():
                f.write(f'{_k}={_v}\n')

    @staticmethod
    def set_report_executer_on_results():
        """
        在allure-results报告的根目录下生成一个写入了执行人的文件：executor.json
        @return:
        """
        from core.config_manager import config
        allure_executor = {
            "name": "local-runner",
            "type": "pytest",
            "buildName": config.project_name(),
            "reportName": "local Allure Report"
        }
        allure_env_file = ALLURE_RESULT / 'executor.json'
        with open(allure_env_file, 'w', encoding='utf-8') as f:
            f.write(str(json.dumps(allure_executor, ensure_ascii=False, indent=4)))


if __name__ == '__main__':
    AllureReportBeautiful.set_report_name('API自动化测试报告')
