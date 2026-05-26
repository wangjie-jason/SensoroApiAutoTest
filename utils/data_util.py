#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/9/11 15:52
# @Author : wangjie
# @File : data_util.py
# @project : SensoroApiAutoTest
import ast
import re
from dataclasses import asdict
from string import Template
from typing import Any, Callable

from utils.jenkins_util import JenkinsUtil
from utils.report_data_handle import ReportDataHandle


class DataProcessor:
    """数据处理与模板替换，使用预注册函数映射表替代 eval 执行"""

    # 注册可在模板中调用的函数
    _function_registry: dict[str, Callable] = {}

    @classmethod
    def register_function(cls, name: str, func: Callable):
        """注册一个可在模板中使用的函数"""
        cls._function_registry[name] = func

    @staticmethod
    def eval_data(data: str) -> Any:
        """安全地将字符串转换为 Python 字面量（列表、字典等）"""
        try:
            return ast.literal_eval(data)
        except (SyntaxError, ValueError, TypeError):
            return data

    def process_data(self, data: Any, source: dict = None) -> Any:
        """
        递归处理数据，支持模板变量替换和注册函数调用。
        :param data: 待处理的数据（字符串、列表或字典）
        :param source: 变量替换的上下文字典
        :return: 处理后的数据
        """
        if source is None:
            source = {}

        if isinstance(data, str):
            return self._process_string(data, source)
        elif isinstance(data, list):
            return [self.process_data(item, source) for item in data]
        elif isinstance(data, dict):
            return {k: self.process_data(v, source) for k, v in data.items()}
        return data

    def _process_string(self, s: str, source: dict) -> Any:
        """
        处理字符串中的模板变量 ${var} 和函数调用 ${func()}。
        使用注册的函数映射表，不调用 eval。
        """
        # Step 1: 替换 ${var} 形式的变量
        s = Template(s).safe_substitute(source)

        # Step 2: 替换 ${func()} 形式的函数调用
        for func_expr in re.findall(r'\$\{(.*?)\}', s):
            try:
                result = self._execute_func(func_expr)
                s = s.replace(f'${{{func_expr}}}', str(result), 1)
            except Exception as e:
                from core.exceptions import DataProcessorError
                raise DataProcessorError(f'函数执行错误: {func_expr}, 错误: {e}')

        return self.eval_data(s)

    @classmethod
    def _execute_func(cls, expr: str) -> Any:
        """
        执行注册的函数表达式，支持 obj.method() 链式调用。
        例如：FakerHelper().random_name()
        """
        # 尝试从注册表中直接查找
        if expr in cls._function_registry:
            return cls._function_registry[expr]()

        # 支持实例方法调用 obj.method()
        if '(' in expr and expr.endswith(')'):
            call_part = expr[:expr.rindex('(')].strip()
            # 解析 obj.method 结构
            if '.' in call_part:
                parts = call_part.split('.')
                obj_name = parts[0].split('(')[0].strip()
                method_name = parts[-1].strip()

                if obj_name in cls._function_registry:
                    obj = cls._function_registry[obj_name]
                    if callable(obj):
                        obj = obj()
                    method = getattr(obj, method_name, None)
                    if callable(method):
                        return method()

        raise NameError(f'函数未注册: {expr}')


# 预注册常用函数
from utils.faker_util import FakerUtil
from utils.time_util import TimeUtil
from core.config_manager import config

DataProcessor.register_function('FakerUtils', FakerUtil)
DataProcessor.register_function('TimeUtil', TimeUtil)
DataProcessor.register_function('config', config)
DataProcessor.register_function('JenkinsUtil', JenkinsUtil)

if __name__ == "__main__":
    data_processor = DataProcessor()

    # ----------------------------------以下是各种测试数据---------------------------------------------
    # 用于替换的模板
    source_data = {
        "name": "John",
        "age": 30,
        "random_int": FakerUtil().random_int()
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
    input_data = '["[1,2,\'3\',4]","${name}","${FakerUtils().random_int()}",${config.current_env()}]'

    # 字符串内套字典,进行模板替换，并执行自定义方法，结果区分int和str类型,返回格式：{'age': 30, 'name': 'John', 'random_name': '王红梅', 'random_str': '2309', 'random_int': 2309} <class 'dict'>
    # input_data = "{'age':${age},'name':'${name}','random_name':'${FakerUtils().random_name()}','random_str':'${FakerUtils().random_int()}','random_int':${FakerUtils().random_int()}}"
    pytest_result = asdict(ReportDataHandle.pytest_json_report_case_count())
    print(DataProcessor().process_data(config.wechat_content(), pytest_result))
    processed_data = data_processor.process_data(input_data, source_data)
    print(processed_data, type(processed_data))
