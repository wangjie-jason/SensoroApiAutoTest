# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/8 19:13
# @Author : wangjie
# @File : jenkins_handle.py
# @project : SensoroApiAutoTest
import os
import shutil

from configs.paths_config import OUT_FILES_DIR
from utils.allure_handle import AllureReportBeautiful


def get_env_from_jenkins(name, base=''):
    """从Jenkins中获取全局环境变量"""
    return os.getenv(name) and os.getenv(name).strip() or base


ProjectName = get_env_from_jenkins("JOB_NAME")  # Jenkins构建项目名称
BUILD_URL = get_env_from_jenkins("BUILD_URL")  # Jenkins构建项目URL
BUILD_NUMBER = get_env_from_jenkins("BUILD_NUMBER")  # Jenkins构建编号
ALLURE_URL = BUILD_URL + 'allure/'  # Jenkins构建的allure报告地址
JENKINS_HOME = get_env_from_jenkins("JENKINS_HOME")  # Jenkins的主目录


def change_jenkins_allure_report_name():
    """从环境变量中读取报告名称并修改Allure报告名称，此方法只针对Jenkins使用allure插件生成的报告"""
    try:
        # 从环境变量中读取报告名称
        new_name = os.getenv('ALLURE_REPORT_NAME',
                             'Allure Report')  # 如果环境变量中没有ALLURE_REPORT_NAME并且未传报告名称参数，默认使用'Allure Report'

        if not new_name:
            raise ValueError("环境变量'ALLURE_REPORT_NAME'未设置或为空。")

        print(f"使用Allure报告名称: {new_name}")

        # 设置Allure报告名称
        AllureReportBeautiful.set_report_name(new_name)

        # 保存压缩文件目标路径（压缩文件将移动到这里）
        zip_path = os.path.join(JENKINS_HOME, 'jobs', ProjectName, 'builds', BUILD_NUMBER, 'archive',
                                'allure-report.zip')

        # 确保压缩文件不存在，如果存在先删除
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"已删除现有zip文件：{zip_path} ")

        # 使用shutil.make_archive压缩整个Allure Report目录并移动到目标目录（OUT_FILES_DIR参数的作用是保留原目录名称）
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', OUT_FILES_DIR, 'allure_report')
        print(f"Allure报告压缩为: {zip_path}")

        # 返回压缩后的文件路径
        return zip_path

    except Exception as e:
        print(f"错误发生: {e}")
        return None


if __name__ == '__main__':
    change_jenkins_allure_report_name()
