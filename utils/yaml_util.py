#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/5 11:48
# @Author : wangjie
# @File : yaml_util.py
# @project : SensoroApiAutoTest
import json
from pathlib import Path
from typing import Union, Dict, Any

import yaml

from core.exceptions import ValueTypeError
from core.paths import BASE_DIR


class YamlUtil:
    """yaml文件相关操作"""

    @staticmethod
    def read_yaml(file_path: Union[str, Path]):
        """
        读取 YAML 文件
        :param file_path: 文件路径（相对路径 / 绝对路径）
        """
        # 自动拼接项目根目录
        path = Path(BASE_DIR) / file_path if not Path(file_path).is_absolute() else Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"YAML 文件不存在：{path}")
        with open(path, 'r', encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(file_path: Union[str, Path], data: Dict[str, Any], mode: str = "w") -> None:
        """
        往yaml文件中写入数据，默认是覆盖写入
        :param file_path: 文件路径
        :param data: 要写入的数据
        :param mode: 写入模式
        """
        path = Path(BASE_DIR) / file_path if not Path(file_path).is_absolute() else Path(file_path)
        with open(path, mode=mode, encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    @staticmethod
    def json_to_yaml(json_or_dict_data: Union[str, Dict]) -> str:
        """
        将json或dict格式的数据转换成yaml格式的数据
        :param json_or_dict_data: 传入json字符串或字典格式数据
        :return:
        """
        try:
            if isinstance(json_or_dict_data, dict):
                # 判断是dict格式，直接将Python字典转换为YAML格式字符串
                yaml_data = yaml.dump(json_or_dict_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
            else:
                # 否则解析JSON字符串为Python字典
                json_data = json.loads(json_or_dict_data)
                # 将Python字典转换为YAML格式字符串
                yaml_data = yaml.dump(json_data, default_flow_style=False, allow_unicode=True, sort_keys=False)

            return yaml_data
        except Exception as e:
            raise ValueTypeError(f"转换失败，请确认传入的数据是否是json格式或字典格式，错误信息: {str(e)}")

    @staticmethod
    def json_to_yaml_file(json_file_path: str, yaml_file_path: str):
        """
        将json文件转换成yaml文件
        :param json_file_path: Json文件路径
        :param yaml_file_path: 需要保存的yaml文件相对路径或绝对路径，相对路径如：data/login.yaml、data/automatic_datas/login.yaml
        :return:
        """
        try:
            # 读取JSON文件内容
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)

            # 打开YAML文件并将YAML格式数据写入
            yaml_file_path = BASE_DIR / yaml_file_path
            with open(yaml_file_path, 'w') as yaml_file:
                yaml.dump(json_data, yaml_file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except Exception as e:
            raise ValueTypeError(
                f"转换失败，请确认传入的文件是否是json数据文件或文件内数据是否是json格式，错误信息：{str(e)}")


if __name__ == '__main__':
    print(YamlUtil.read_yaml('data/user.yaml'))
    data_user = YamlUtil.read_yaml('data/user.yaml')
    params = [(item['case_title'], item.get('user_id')) for item in data_user]
    print(params)

    # 示例JSON数据
    json_string = '{"name": "John", "age": 30, "city": "New York"}'

    # 调用方法进行转换
    yaml_result = YamlUtil.json_to_yaml(json_string)
    print(yaml_result)
    print(YamlUtil.read_yaml('config/environments.yaml'))
