# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/2 14:44
# @Author : wangjie
# @File : get_config.py
# @project : SensoroApi
import configparser
import os.path

from utils.get_dir_path import GetPath


def get_config(file_name):
    """读取config配置文件"""
    # path = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(path, '../configs', file_name)

    file_path = os.path.join(GetPath.get_configs_path(), file_name)

    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")
    return config


if __name__ == '__main__':
    config = get_config('lins_environment.ini')
    print(config['test']['host'])
