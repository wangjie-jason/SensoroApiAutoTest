#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import yaml


def get_yaml_data(dir_file_name):
    """获取yaml文件的内容"""
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(path, '../'))

    with open(file_path + '/' + dir_file_name, 'r', encoding='utf-8') as f:
        datas = yaml.safe_load(f)
        return datas
