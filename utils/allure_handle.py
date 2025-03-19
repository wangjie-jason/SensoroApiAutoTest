#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/27 20:05
# @Author : wangjie
# @File : allure_handle.py
# @project : SensoroApiAutoTest
import json
import os
import platform

import allure
import pytest
from requests.structures import CaseInsensitiveDict

from common.models import AllureAttachmentType
from configs.paths_config import TEMP_DIR, ALLURE_REPORT_DIR


def allure_title(title: str) -> None:
    """allure中动态生成用例标题"""
    # allure.dynamic动态属性
    allure.dynamic.title(title)


def allure_attach_text(name: str, body: str = None) -> None:
    """
    allure报告添加文本格式附件
    :param name: 附件名称
    :param body: 附件内容
    :return:
    """
    # 确保 body 是字符串类型
    if body is None:
        body = "None"  # 如果 body 为 None，设置为空字符串
    elif not isinstance(body, str):
        body = str(body)  # 如果 body 不是字符串，强制转换为字符串
    allure.attach(body=body, name=name, attachment_type=allure.attachment_type.TEXT)


def allure_attach_json(name: str, body: str | dict | CaseInsensitiveDict | None = None) -> None:
    """
    allure报告添加json格式附件
    :param name: 附件名称
    :param body: 附件内容
    :return:
    """
    # 检查是否是 CaseInsensitiveDict 类型
    if isinstance(body, CaseInsensitiveDict):
        body = dict(body)  # 将CaseInsensitiveDict 转换为普通字典，一般请求头或者响应头是这种格式
    # 尝试格式化 JSON
    try:
        if isinstance(body, dict):
            # 如果 body 是字典直接转换
            body = json.dumps(body, ensure_ascii=False, indent=4)
        elif body is None:
            # 如果 body 为 None，设置为空字符串
            body = "None"
        elif isinstance(body, str):
            # 如果是字符串，先尝试转成字典，再解析成JSON
            body = json.dumps(json.loads(body), indent=4, ensure_ascii=False)
        else:
            # 其他类型，直接传原始数据
            body = body
    except (json.JSONDecodeError, TypeError):
        body = body  # 解析失败，直接传原始数据
    allure.attach(body=body, name=name, attachment_type=allure.attachment_type.JSON)


def allure_attach_file(name: str, source: str):
    """
    allure报告上传附件、图片、excel等
    :param name: 名称
    :param source: 文件路径，相当于传一个文件
    :return:
    """
    # 检查文件是否存在
    if not os.path.isfile(source):
        raise f"文件不存在: {source}"

    # 获取上传附件的尾缀，判断对应的 attachment_type 枚举值
    _name = source.split('.')[-1].lower()

    # 动态生成映射字典
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
        report_title_filepath = os.path.join(ALLURE_REPORT_DIR, "index.html")
        # 定义为只读模型，并定义名称为: f
        with open(report_title_filepath, 'r+', encoding="utf-8") as f:
            # 读取当前文件的所有内容
            all_the_lines = f.readlines()
            f.seek(0)
            f.truncate()
            # 循环遍历每一行的内容，将 "Allure Report" 全部替换为 → new_title(新文案)
            for line in all_the_lines:
                f.write(line.replace("Allure Report", new_title))
            # 关闭文件
            f.close()

    @staticmethod
    def set_report_name(new_name):
        """
        修改Allure报告Overview的标题文案
        @param new_name:  需要更改的标题文案 【 原文案为：ALLURE REPORT 】
        @return:
        """
        title_filepath = os.path.join(ALLURE_REPORT_DIR, "widgets", "summary.json")
        # 检查summary.json文件是否存在
        if not os.path.exists(title_filepath):
            raise FileNotFoundError(f"修改报告名称时，summary.json文件未找到： {title_filepath}")
        # 读取summary.json中的内容
        with open(title_filepath, 'r', encoding='utf-8') as f:
            params = json.load(f)
        # 修改报告名称
        params['reportName'] = new_name
        # 将修改后的内容写回summary.json
        with open(title_filepath, 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False, indent=4)

    @staticmethod
    def set_report_env_on_results():
        """
        在allure-results报告的根目录下生成一个写入了环境信息的文件：environment.properties(注意：不能放置中文，否则会出现乱码)
        @return:
        """
        # 方法内导入，防止其他文件引用allure_handle文件时引发循环导入问题
        from common.settings import ENV
        from configs.env_config import EnvConfig
        # 需要写入的环境信息
        allure_env = {
            'OperatingEnvironment': ENV,
            'BaseUrl': EnvConfig.URL(),
            'PythonVersion': platform.python_version(),
            'Platform': platform.platform(),
            'PytestVersion': pytest.__version__,
        }
        allure_env_file = os.path.join(TEMP_DIR, 'environment.properties')
        with open(allure_env_file, 'w', encoding='utf-8') as f:
            for _k, _v in allure_env.items():
                f.write(f'{_k}={_v}\n')

    @staticmethod
    def set_report_executer_on_results():
        """
        在allure-results报告的根目录下生成一个写入了执行人的文件：executor.json
        @return:
        """
        # 需要写入的环境信息
        allure_executor = {
            "name": "汪杰",
            "type": "jenkins",
            "url": "http://helloqa.com",
            "buildOrder": 3,
            "buildName": "allure-report_deploy#1",
            "buildUrl": "http://helloqa.com#1",
            "reportUrl": "http://helloqa.com#1/AllureReport",
            "reportName": "汪杰 Allure Report"
        }
        allure_env_file = os.path.join(TEMP_DIR, 'executor.json')
        with open(allure_env_file, 'w', encoding='utf-8') as f:
            f.write(str(json.dumps(allure_executor, ensure_ascii=False, indent=4)))


if __name__ == '__main__':
    AllureReportBeautiful.set_report_name('API自动化测试报告')
