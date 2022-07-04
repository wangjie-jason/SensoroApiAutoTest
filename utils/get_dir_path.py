# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/4 15:26
# @Author : wangjie
# @File : get_dir_path.py
# @project : SensoroApi
from configs.dir_path_config import BASE_DIR, COMMON_DIR, CONFIGS_DIR, DATAS_DIR, PAGE_API_DIR, TEST_CASE_DIR, UTILS_DIR


class GetPath:
    """
    获取文件路径
    """

    @staticmethod
    def get_project_path():
        """获取项目工程路径"""
        return BASE_DIR

    @staticmethod
    def get_common_path():
        """获取common目录路径"""
        return COMMON_DIR

    @staticmethod
    def get_configs_path():
        """获取configs目录路径"""
        return CONFIGS_DIR

    @staticmethod
    def get_datas_path():
        """获取datas目录路径"""
        return DATAS_DIR

    @staticmethod
    def get_page_api_path():
        """获取pageApi目录路径"""
        return PAGE_API_DIR

    @staticmethod
    def get_test_case_path():
        """获取testCase目录路径"""
        return TEST_CASE_DIR

    @staticmethod
    def get_utils_path():
        """获取utils目录路径"""
        return UTILS_DIR


if __name__ == '__main__':
    print(GetPath.get_datas_path())
