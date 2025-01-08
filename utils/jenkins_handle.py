# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/8 19:13
# @Author : wangjie
# @File : jenkins_handle.py
# @project : SensoroApiAutoTest
import json
import os
import shutil
import tempfile
import zipfile

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


def modify_jenkins_allure_report_name_in_zip():
    """
    直接修改Jenkins构建归档中的allure-report.zip压缩包的报告名称，然后重新压缩，相比较于上面的change_jenkins_allure_report_name方法的好处是直接在原压缩包内修改
    :return:
    """
    # 从环境变量中读取报告名称
    new_name = os.getenv('ALLURE_REPORT_NAME',
                         'Allure Report')  # 如果环境变量中没有ALLURE_REPORT_NAME并且未传报告名称参数，默认使用'Allure Report'

    # 找到zip文件路径
    zip_path = os.path.join(JENKINS_HOME, 'jobs', ProjectName, 'builds', BUILD_NUMBER, 'archive',
                            'allure-report.zip')

    # 检查allure-report.zip压缩包是否存在
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"allure-report.zip压缩包未找到：{zip_path}")

    # 临时文件夹用于存放解压后的内容
    with tempfile.TemporaryDirectory() as temp_dir:
        # 打开并提取 zip 文件
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 定义需要修改的文件路径
        summary_file_path = os.path.join(temp_dir, 'allure_report', 'widgets', 'summary.json')

        # 检查 summary.json 是否存在
        if not os.path.exists(summary_file_path):
            raise FileNotFoundError(f"在zip归档文件中找不到summary.json文件：{summary_file_path}")

        # 读取原始 summary.json
        with open(summary_file_path, 'r', encoding='utf-8') as file:
            summary_data = json.load(file)

        # 修改 summary.json 的内容
        summary_data['reportName'] = new_name

        # 保存修改后的 summary.json
        with open(summary_file_path, 'w', encoding='utf-8') as file:
            json.dump(summary_data, file, indent=4, ensure_ascii=False)

        # 创建一个新的 zip 文件，并将修改后的文件重新压缩
        new_zip_path = zip_path.replace('.zip', '.zip')
        with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            # 遍历解压后的文件夹，重新压缩成一个新的 zip 文件
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    # 设置正确的 arcname，以保持 zip 文件的原有结构
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_ref.write(file_path, arcname)

        print(f"修改后重新压缩zip文件: {new_zip_path}")
        return new_zip_path


if __name__ == '__main__':
    # change_jenkins_allure_report_name()
    modify_jenkins_allure_report_name_in_zip()
