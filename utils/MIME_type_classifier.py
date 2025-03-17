#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/11/30 16:57
# @Author : wangjie
# @File : MIME_type_classifier.py
# @project : SensoroApiAutoTest
from common.models import MIMEFileType

d = {
    'image/png': ['png'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['xlsx'],
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['pptx'],
    'application/pdf': ['pdf'],
    'image/jpeg': ['jpg', 'jpeg'],
    'application/zip': ['zip'],
    'text/plain': ['txt'],
    'video/mp4': ['mp4'],
    'application/msword': ['doc', 'dot'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': ['dotx'],
    'application/vnd.ms-word.document.macroEnabled.12': ['docm'],
    'application/vnd.ms-word.template.macroEnabled.12': ['dotm'],
    'application/vnd.ms-excel': ['xls', 'xlt', 'xla'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template': ['xltx'],
    'application/vnd.ms-excel.sheet.macroEnabled.12': ['xlsm'],
    'application/vnd.ms-excel.template.macroEnabled.12': ['xltm'],
    'application/vnd.ms-excel.addin.macroEnabled.12': ['xlam'],
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12': ['xlsb'],
    'application/vnd.ms-powerpoint': ['ppt', 'pot', 'pps', 'ppa'],
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': ['ppsx'],
    'application/vnd.ms-powerpoint.addin.macroEnabled.12': ['ppam'],
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12': ['pptm', 'potm'],
    'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': ['ppsm'],
    'application/x-tar': ['tar'],
}


def get_MIME(file_name):
    """
    多用途互联网邮件扩展类型,根据文件后缀匹配文件类型并返回相应的 MIME 类型。
    :param file_name:文件名或者文件路径
    :return:对应的 MIME 类型
    """

    extension = file_name.split('.')[-1].lower()

    for file_type in MIMEFileType:
        if extension in file_type.value[1]:
            return file_type.value[0]

    return 'application/octet-stream'  # 一切未知类型


if __name__ == '__main__':
    mime_type = get_MIME('example.png')
    print(mime_type)


