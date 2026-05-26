#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/8 16:14
# @Author : wangjie
# @File : jenkins_util.py
# @project : SensoroApiAutoTest
import json
import os
import tempfile
import zipfile


class JenkinsUtil:
    """读取 Jenkins 环境变量"""

    @staticmethod
    def get_project_name() -> str:
        """获取Jenkins构建项目名称"""
        return os.environ.get('JOB_NAME', '')

    @staticmethod
    def get_build_url() -> str:
        """Jenkins构建项目URL"""
        return os.environ.get('BUILD_URL', '')

    @staticmethod
    def get_build_number() -> str:
        """获取Jenkins构建编号"""
        return os.environ.get('BUILD_NUMBER', 'local')

    @staticmethod
    def get_jenkins_home() -> str:
        """获取Jenkins的主目录"""
        return os.environ.get('JENKINS_HOME', '')

    @staticmethod
    def get_allure_url() -> str:
        """获取Jenkins构建的allure报告地址"""
        build_url = os.environ.get('BUILD_URL', '')
        if build_url:
            return build_url + 'allure'
        return ''

    def modify_jenkins_allure_report_name_in_zip(self):
        """
        直接修改Jenkins构建归档中的allure-report.zip压缩包的报告名称，然后重新压缩，相比较于上面的change_jenkins_allure_report_name方法的好处是直接在原压缩包内修改
        :return:
        """
        # 从环境变量中读取报告名称
        new_name = os.getenv('ALLURE_REPORT_NAME',
                             'Allure Report')  # 如果环境变量中没有ALLURE_REPORT_NAME并且未传报告名称参数，默认使用'Allure Report'

        # 找到zip文件路径
        zip_path = os.path.join(self.get_jenkins_home(), 'jobs', self.get_project_name(), 'builds',
                                self.get_build_number(), 'archive',
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
    JenkinsUtil().modify_jenkins_allure_report_name_in_zip()
