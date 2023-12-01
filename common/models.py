# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 15:23
# @Author : wangjie
# @File : models.py
# @project : SensoroApi
from dataclasses import dataclass
from enum import Enum, unique
from typing import Text, List, Union

from pydantic import BaseModel


class Environment(Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
    DIANJUN = 'dianjun'


@dataclass
class TestMetrics:
    """ 用例结果数据 """
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


class Method(Enum):
    """
    请求方式
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


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


class Email(BaseModel):
    mail_subject: Union[Text, None] = None  # 邮件标题
    sender_username: Text  # 发件人邮箱
    sender_password: Text  # 发件人邮箱授权码
    receiver_mail_list: List[Text]  # 收件人邮箱
    smtp_domain: Text  # 发送邮箱的域名
    smtp_port: Union[int, None] = None  # 发送邮箱的端口号


class MIMEFileType(Enum):
    PNG = ('image/png', ['png'])
    XLSX = ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ['xlsx'])
    PPTX = ('application/vnd.openxmlformats-officedocument.presentationml.presentation', ['pptx'])
    PDF = ('application/pdf', ['pdf'])
    JPG = ('image/jpeg', ['jpg', 'jpeg'])
    ZIP = ('application/zip', ['zip'])
    TXT = ('text/plain', ['txt'])
    MP4 = ('video/mp4', ['mp4'])
    DOC = ('application/msword', ['doc', 'dot'])
    DOCX = ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', ['docx'])
    DOTX = ('application/vnd.openxmlformats-officedocument.wordprocessingml.template', ['dotx'])
    DOCM = ('application/vnd.ms-word.document.macroEnabled.12', ['docm'])
    DOTM = ('application/vnd.ms-word.template.macroEnabled.12', ['dotm'])
    XLS = ('application/vnd.ms-excel', ['xls', 'xlt', 'xla'])
    XLTX = ('application/vnd.openxmlformats-officedocument.spreadsheetml.template', ['xltx'])
    XLSM = ('application/vnd.ms-excel.sheet.macroEnabled.12', ['xlsm'])
    XLTM = ('application/vnd.ms-excel.template.macroEnabled.12', ['xltm'])
    XLAM = ('application/vnd.ms-excel.addin.macroEnabled.12', ['xlam'])
    XLSB = ('application/vnd.ms-excel.sheet.binary.macroEnabled.12', ['xlsb'])
    PPT = ('application/vnd.ms-powerpoint', ['ppt', 'pot', 'pps', 'ppa'])
    PPSX = ('application/vnd.openxmlformats-officedocument.presentationml.slideshow', ['ppsx'])
    PPAM = ('application/vnd.ms-powerpoint.addin.macroEnabled.12', ['ppam'])
    PPTM = ('application/vnd.ms-powerpoint.presentation.macroEnabled.12', ['pptm', 'potm'])
    PPSM = ('application/vnd.ms-powerpoint.slideshow.macroEnabled.12', ['ppsm'])
    TAR = ('application/x-tar', ['tar'])


if __name__ == '__main__':
    print(Environment.DEV.name)
    print(Environment.DEV.value)
