# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 20:53
# @Author : wangjie
# @File : base_log.py
# @project : SensoroApi

import logging
import os.path
import sys
import time

import colorlog

from common.settings import LOG_DEBUG, LOG_CONSOLE
from configs.dir_path_config import LOGS_DIR


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

            # 设置日志输出格式
            # 设置写入文件时的格式
            formatter_file = logging.Formatter(
                '%(levelname)-9s%(asctime)s-%(filename)s[line:%(lineno)d]：%(message)s', '%Y-%m-%d %H:%m:%S'
            )
            # 设置终端上显示带颜色的格式
            formatter_stream = cls.log_color()

            # 设置日志存储路径
            if not cls._log_path:
                cls._log_path = cls.generate_log_path()

            # 创建FileHandler,用于写入日志
            fh = cls.create_file_handler(formatter_file)

            # 创建StreamHandler,用于输出到控制台
            ch = cls.create_console_handler(formatter_stream)

            # 添加输出
            logger.addHandler(ch)
            logger.addHandler(fh)

            # 控制日志级别
            cls.configure_log_levels(logger, ch, fh)

            # 将创建的日志记录器实例赋值给类变量 _logger_instance，以实现单例模式
            cls._logger_instance = logger

            return cls._logger_instance

    @classmethod
    def generate_log_path(cls):
        log_dir_today = os.path.join(LOGS_DIR, time.strftime('%Y-%m-%d'))
        if not os.path.exists(log_dir_today):
            os.makedirs(log_dir_today)
        now = time.strftime('%Y-%m-%d_%H:%M:%S')
        if sys.platform in ('win32', 'win64'):  # 兼容window文件命名时不支持":"的方式
            separator = '_'
        else:
            separator = ':'
        return os.path.join(log_dir_today, f"{now.replace(':', separator)}-log.log")

    @classmethod
    def create_file_handler(cls, formatter):
        fh = logging.FileHandler(cls._log_path, encoding='utf-8')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        return fh

    @classmethod
    def create_console_handler(cls, formatter):
        if LOG_CONSOLE:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            ch.setLevel(logging.INFO)
            return ch
        else:
            return logging.NullHandler()

    @classmethod
    def configure_log_levels(cls, logger, ch, fh):
        level = logging.DEBUG if LOG_DEBUG else logging.INFO
        logger.setLevel(level)
        fh.setLevel(level)
        ch.setLevel(level)

    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red,bg_bold_white',
        }

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)-9s%(asctime)s-%(filename)s[line:%(lineno)d]：%(message)s', '%Y-%m-%d %H:%m:%S',
            log_colors=log_colors_config
        )
        return formatter


logger = Logger().get_logger()

if __name__ == '__main__':
    logger.debug("测试日志")
    logger.info("测试日志")
    logger.warning("测试日志")
    logger.error("测试日志")
    logger.critical("测试日志")
