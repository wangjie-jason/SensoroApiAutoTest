#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import yaml

from utils.get_dir_path import GetPath


def get_yaml_data(dir_file_name):
    """获取yaml文件的内容"""
    # path = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.abspath(os.path.join(path, '../'))

    file_path = os.path.join(GetPath.get_project_path(), dir_file_name)

    with open(file_path, 'r', encoding='utf-8') as f:
        datas = yaml.safe_load(f)
        return datas


if __name__ == '__main__':
    print(get_yaml_data('datas/login.yaml'))
