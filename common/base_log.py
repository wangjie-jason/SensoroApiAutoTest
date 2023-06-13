# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 20:53
# @Author : wangjie
# @File : base_log.py
# @project : SensoroApi

import logging
import os.path
import time

from common.settings import LOG_DEBUG


class Logger:
    """用于全局记录log"""
    _logger_instance = None
    _log_path = None

    @classmethod
    def get_logger(cls):
        """单例模式,使多文件或多次调用时,始终使用这一个logger"""
        if cls._logger_instance:
            return cls._logger_instance
        else:
            logger = logging.getLogger()

            # 设置日志默认可输出的最低等级
            logger.setLevel(logging.INFO)

            # 设置日志输入格式
            format_ = logging.Formatter(
                '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s-%(message)s'
            )

            # 设置日志存储路径
            if not cls._log_path:
                file_path = os.path.abspath(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../outFiles/logs'))
                dir_name = time.strftime('%Y-%m-%d')
                file_name = time.strftime('%Y-%m-%d %H:%M:%S') + '-' + 'log.log'
                if not os.path.exists(os.path.join(file_path, dir_name)):
                    os.makedirs(os.path.join(file_path, dir_name))
                cls._log_path = os.path.join(file_path, dir_name, file_name)

            # 创建FileHandler,用于写入日志
            fh = logging.FileHandler(cls._log_path, encoding='utf-8')
            fh.setFormatter(format_)
            fh.setLevel(logging.INFO)

            # 创建StreamHandler,用于输出到控制台
            ch = logging.StreamHandler()
            ch.setFormatter(format_)
            ch.setLevel(logging.INFO)

            # 添加输出
            logger.addHandler(ch)
            logger.addHandler(fh)

            # 控制日志级别
            if LOG_DEBUG:
                logger.setLevel(logging.DEBUG)
                ch.setLevel(logging.DEBUG)
                fh.setLevel(logging.DEBUG)

            cls._logger_instance = logger

            return cls._logger_instance


logger = Logger().get_logger()

if __name__ == '__main__':
    logger.info("测试日志")
