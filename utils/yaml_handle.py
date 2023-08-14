#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os
import yaml

from common.exceptions import ValueTypeError
from configs.dir_path_config import BASE_DIR


class YamlHandle:
    """yaml文件相关操作"""

    def __init__(self, dir_file_name):
        """
        :param dir_file_name: 项目下文件所在目录名及文件名，如：datas/login.yaml、datas/automatic_datas/login.yaml，也可以传绝对路径
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

    @staticmethod
    def json_to_yaml(json_or_dict_data):
        """
        将json或dict格式的数据转换成yaml格式的数据
        :param json_or_dict_data: 传入json字符串或字典格式数据
        :return:
        """
        try:
            if isinstance(json_or_dict_data, dict):
                # 判断是dict格式，直接将Python字典转换为YAML格式字符串
                yaml_data = yaml.dump(json_or_dict_data, default_flow_style=False)
            else:
                # 否则解析JSON字符串为Python字典
                json_data = json.loads(json_or_dict_data)
                # 将Python字典转换为YAML格式字符串
                yaml_data = yaml.dump(json_data, default_flow_style=False)

            return yaml_data
        except Exception as e:
            raise ValueTypeError(f"转换失败，请确认传入的数据是否是json格式或字典格式，错误信息: {str(e)}")

    def json_to_yaml_file(self, yaml_file_path):
        """
        将json文件转换成yaml文件
        :param yaml_file_path: 需要保存的yaml文件相对路径或绝对路径，相对路径如：datas/login.yaml、datas/automatic_datas/login.yaml
        :return:
        """
        try:
            # 读取JSON文件内容
            with open(self.file_path, 'r') as json_file:
                json_data = json.load(json_file)

            # 打开YAML文件并将YAML格式数据写入
            yaml_file_path = os.path.join(BASE_DIR, yaml_file_path)
            with open(yaml_file_path, 'w') as yaml_file:
                yaml.dump(json_data, yaml_file, default_flow_style=False)
        except Exception as e:
            raise ValueTypeError(f"转换失败，请确认传入的文件是否是json数据文件或文件内数据是否是json格式，错误信息：{str(e)}")


if __name__ == '__main__':
    # print(YamlHandle('datas/login.yaml').read_yaml())
    # data_smsCode = YamlHandle('datas/login.yaml').read_yaml()
    # params = [(item['phone'], item['smsCode'], item['expected']) for item in data_smsCode]
    # print(params)

    # 示例JSON数据
    json_string = '{"name": "John", "age": 30, "city": "New York"}'

    # 调用方法进行转换
    yaml_result = YamlHandle.json_to_yaml(json_string)
    print(yaml_result)
