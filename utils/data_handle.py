# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/12 16:36
# @Author : wangjie
# @File : data_handle.py
# @project : SensoroApiAutoTest
import ast
import random
import re
from string import Template
from typing import Any

from common.exceptions import DataProcessorFuncError
from utils.faker_utils import FakerUtils
from utils.time_utils import TimeUtil


class DataProcessor:

    def process_data(self, data: Any, source=None) -> Any:
        """
        处理输入的数据，根据数据类型分发到不同的处理方法中。
        :param data: 输入的数据，可以是字符串、列表或字典。
        :param source: 数据源，用于字符串模板替换。
        :return: 处理后的数据
        """
        if source is None:
            source = {}
        if isinstance(data, str):
            data = self.process_string(data, source)
        elif isinstance(data, list):
            data = [self.process_data(item, source) for item in data]
        elif isinstance(data, dict):
            data = {key: self.process_data(value, source) for key, value in data.items()}
        return data

    def eval_data(self, data: Any) -> Any:
        """
        尝试解析输入的数据，使用ast.literal_eval模块，只会执行合法的Python表达式，例如将："[1,2,3]" 或者"{'k':'v'}" -> [1,2,3], {'k':'v'}可以执行，'1+1'这种不会执行
        :param data: 输入的数据，通常是一个字符串。
        :return: 解析后的数据，如果无法解析则返回原始输入数据。
        """
        try:
            return ast.literal_eval(data)
        except (SyntaxError, ValueError, TypeError):
            return data

    def process_string(self, s: str, source: dict) -> str:
        """
        处理输入的字符串，包括变量替换和函数执行。
        :param s: 输入的字符串，可能包含变量和函数调用。
        :param source: 数据源，用于字符串模板替换。
        :return: 处理后的字符串
        """
        s = Template(s).safe_substitute(source)
        for func in re.findall('\\${(.*?)}', s):
            try:
                s = s.replace('${%s}' % func, str(eval(func)), 1)
            except NameError:
                # 处理未定义的变量或函数
                raise DataProcessorFuncError(
                    f'方法执行错误，请检查data_handle.py中是否导入该方法，或者方法名称是否正确，方法名：{func}')
            except Exception as e:
                # 处理其他异常情况
                raise DataProcessorFuncError(
                    f'方法执行错误：{func}, 报错信息：{e}')
        return self.eval_data(s)


if __name__ == "__main__":
    data_processor = DataProcessor()

    # ----------------------------------以下是各种测试数据---------------------------------------------
    # 用于替换的模板
    source_data = {
        "name": "John",
        "age": 30,
        "random_int": FakerUtils().random_int()
    }

    # 字典内进行模板替换，并且执行自定义方法,结果区分int和str类型,返回格式：{'message': "Hello, 吕亮! Your age is 30. Random number_int: 1515.Random number_str: '2637'", 'nested_data': ["This is John's data.", {'message': 'Age: 30.', 'nested_list': ['More data: 677.']}]} <class 'dict'>
    input_data = {
        "message": "Hello, ${FakerUtils().random_name()}! Your age is ${age}. Random number_int: ${FakerUtils().random_int()}.Random number_str: '${FakerUtils().random_int()}'",
        "nested_data": [
            "This is ${name}'s data.",
            {
                "message": "Age: ${age}.",
                "nested_list": [
                    "More data: ${random_int}.",
                ]
            }
        ]
    }

    # 列表内执行方法,结果区分int和str类型,返回格式：[[1, 2, '3', 4], '张龙', 125, '2275'] <class 'list'>
    # input_data = [[1, 2, "'3'", 4], '${FakerUtils().random_name()}', '${FakerUtils().random_int()}',"'${FakerUtils().random_int()}'"]

    # 字符串内进行模板替换，并执行自定义方法，返回格式：Hello, 李佳! Your age is 30. Random number: 86. <class 'str'>
    # input_data = "Hello, ${FakerUtils().random_name()}! Your age is ${age}. Random number: ${FakerUtils().random_int()}."

    # 字符串内套列表，进行模板替换，并执行自定义方法，结果区分int和str类型,返回格式：['[1,2,'3',4]', 'John', '1615', 4832] <class 'list'>
    # input_data = '["[1,2,\'3\',4]","${name}","${FakerUtils().random_int()}",${FakerUtils().random_int()}]'

    # 字符串内套字典,进行模板替换，并执行自定义方法，结果区分int和str类型,返回格式：{'age': 30, 'name': 'John', 'random_name': '王红梅', 'random_str': '2309', 'random_int': 2309} <class 'dict'>
    # input_data = "{'age':${age},'name':'${name}','random_name':'${FakerUtils().random_name()}','random_str':'${FakerUtils().random_int()}','random_int':${FakerUtils().random_int()}}"
    processed_data = data_processor.process_data(input_data, source_data)
    print(processed_data, type(processed_data))
