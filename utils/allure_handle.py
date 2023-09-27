# !/usr/bin/python
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

from common.models import AllureAttachmentType
from common.settings import ENV
from configs.dir_path_config import TEMP_DIR, ALLURE_REPORT_DIR
from configs.lins_environment import EntryPoint


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
    allure.attach(body=body, name=name, attachment_type=allure.attachment_type.TEXT)


def allure_attach_json(name: str, body: str = None) -> None:
    """
    allure报告添加json格式附件
    :param name: 附件名称
    :param body: 附件内容
    :return:
    """
    allure.attach(body=body, name=name, attachment_type=allure.attachment_type.JSON)


def allure_attach_file(name: str, source: str):
    """
    allure报告上传附件、图片、excel等
    :param name: 名称
    :param source: 文件路径，相当于传一个文件
    :return:
    """
    # 获取上传附件的尾缀，判断对应的 attachment_type 枚举值
    _name = source.split('.')[-1]
    if _name == "txt" or _name == "uri":
        _name = "text" if _name == "txt" else "uri_list"
    attachment_type_mapping = {
        AllureAttachmentType.TEXT: allure.attachment_type.TEXT,
        AllureAttachmentType.CSV: allure.attachment_type.CSV,
        AllureAttachmentType.TSV: allure.attachment_type.TSV,
        AllureAttachmentType.URI_LIST: allure.attachment_type.URI_LIST,
        AllureAttachmentType.HTML: allure.attachment_type.HTML,
        AllureAttachmentType.XML: allure.attachment_type.XML,
        AllureAttachmentType.JSON: allure.attachment_type.JSON,
        AllureAttachmentType.YAML: allure.attachment_type.YAML,
        AllureAttachmentType.PCAP: allure.attachment_type.PCAP,
        AllureAttachmentType.PNG: allure.attachment_type.PNG,
        AllureAttachmentType.JPG: allure.attachment_type.JPG,
        AllureAttachmentType.SVG: allure.attachment_type.SVG,
        AllureAttachmentType.GIF: allure.attachment_type.GIF,
        AllureAttachmentType.BMP: allure.attachment_type.BMP,
        AllureAttachmentType.TIFF: allure.attachment_type.TIFF,
        AllureAttachmentType.MP4: allure.attachment_type.MP4,
        AllureAttachmentType.OGG: allure.attachment_type.OGG,
        AllureAttachmentType.WEBM: allure.attachment_type.WEBM,
        AllureAttachmentType.PDF: allure.attachment_type.PDF, }
    _attachment_type = attachment_type_mapping.get(getattr(AllureAttachmentType, _name.upper(), None), None)
    allure.attach.file(source=source, name=name,
                       attachment_type=_attachment_type,
                       extension=_name)


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
        # 读取summary.json中的json数据，并改写reportName
        with open(title_filepath, 'rb') as f:
            # 加载json文件中的内容给params
            params = json.load(f)
            # 修改内容
            params['reportName'] = new_name
            # 将修改后的内容保存在dict中
            new_params = params
        # 往summary.json中，覆盖写入新的json数据
        with open(title_filepath, 'w', encoding="utf-8") as f:
            json.dump(new_params, f, ensure_ascii=False, indent=4)

    @staticmethod
    def set_report_env_on_results():
        """
        在allure-results报告的根目录下生成一个写入了环境信息的文件：environment.properties(注意：不能放置中文，否则会出现乱码)
        @return:
        """
        # 需要写入的环境信息
        allure_env = {
            'OperatingEnvironment': ENV.name,
            'BaseUrl': EntryPoint.URL(),
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
