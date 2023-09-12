# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/12 16:36
# @Author : wangjie
# @File : data_handle.py
# @project : SensoroApiAutoTest
import ast
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
        data = self.eval_data(data)
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
                func_result = eval(func)
                s = s.replace('${%s}' % func, repr(func_result) if isinstance(func_result, str) else str(func_result))
            except NameError:
                # 处理未定义的变量或函数
                raise DataProcessorFuncError(
                    f'方法执行错误，请检查data_handle.py中是否导入该方法，或者方法名称是否正确，方法名：{func}')
            except Exception as e:
                # 处理其他异常情况
                raise DataProcessorFuncError(
                    f'方法执行错误：{func}, 报错信息：{e}')

        return self.eval_data(s)


# 示例用法
if __name__ == "__main__":
    data_processor = DataProcessor()
    source_data = {
        "name": "John",
        "age": 30,
        "random_int": FakerUtils().random_int()
    }
    input_data = {
        "message": "Hello, ${FakerUtils().random_name()}! Your age is ${age}. Random number: ${FakerUtils().random_int()}.",
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
    # input_data = '[[1,2,3,4],${FakerUtils().random_name()}]'
    # input_data = '${FakerUtils().random_name()}'
    # input_data = "Hello, ${FakerUtils().random_name()}! Your age is ${age}. Random number: ${FakerUtils().random_int()}."
    # input_data = [[1, 2, 3, 4], '${FakerUtils().random_name()}']
    processed_data = data_processor.process_data(input_data, source_data)
    print(processed_data, type(processed_data))
