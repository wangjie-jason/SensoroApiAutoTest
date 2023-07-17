#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import yaml

from configs.dir_path_config import BASE_DIR


class YamlHandle:
    """yaml文件相关操作"""

    def __init__(self, dir_file_name):
        """
        :param dir_file_name: 项目下文件所在目录名及文件名，如：datas/login.yaml、datas/automatic_datas/login.yaml
        """
        file_path = os.path.join(BASE_DIR, dir_file_name)
        self.file_path = file_path

    def read_yaml(self):
        """
        获取yaml文件的数据
        :return:
        """
        with open(file=self.file_path, mode="r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def write(self, data, mode="a"):
        """
        往yaml文件中写入数据，默认是追加写入
        :param data: 要写入的数据
        :param mode: 写入模式
        :return:
        """
        with open(self.file_path, mode=mode, encoding="utf-8") as f:
            yaml.dump(data, f)


if __name__ == '__main__':
    print(YamlHandle('datas/login.yaml').read_yaml())
    data_smsCode = YamlHandle('datas/login.yaml').read_yaml()
    params = [(item['phone'], item['smsCode'], item['expected']) for item in data_smsCode]
    print(params)
