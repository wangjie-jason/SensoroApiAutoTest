# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 15:23
# @Author : wangjie
# @File : models.py
# @project : SensoroApi
from dataclasses import dataclass
from enum import Enum, unique
from typing import Text


class Environment(Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
    DIANJUN = 'dianjun'


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    total: int
    passed: int
    failed: int
    skipped: int
    xfailed: int
    xpassed: int
    error: int
    pass_rate: float
    start_time: Text
    duration: float


if __name__ == '__main__':
    print(Environment.DEV.name)
    print(Environment.DEV.value)


@unique  # 枚举类装饰器，确保只有一个名称绑定到任何一个值。
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"
