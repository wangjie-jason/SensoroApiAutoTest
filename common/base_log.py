# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 20:53
# @Author : wangjie
# @File : base_log.py
# @project : SensoroApi

# TODO:1.添加日志记录器 2.添加邮件发送功能 3.更改base_api的请求方式
import logging
import os.path
import time


class Logger:
    """用于全局记录log"""
    logger_instance = None

    @classmethod
    def get_logger(cls):
        """单例模式,使多文件或多次调用时,始终使用这一个logger"""
        if cls.logger_instance:
            return cls.logger_instance
        else:
            logger = logging.getLogger()

            # 设置日志可输出的最低等级
            logger.setLevel(logging.DEBUG)
            # 设置日志输入格式
            format_ = logging.Formatter(
                '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s-%(message)s'
            )

            # 设置日志存储路径
            file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../outFiles/logs'))
            dir_name = time.strftime('%Y-%m-%d')
            file_name = time.strftime('%Y-%m-%d %H:%M:%S') + '-' + 'log.log'
            if not os.path.exists(os.path.join(file_path, dir_name)):
                os.mkdir(os.path.join(file_path, dir_name))
            log_path = os.path.join(file_path, dir_name, file_name)

            # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志（不使用此方法的原因：有可能第三方库先写入handlers，导致自己的handlers写不进去，无法记录log）
            # if not logger.handlers:
            # 创建FileHandler,用于写入日志
            fh = logging.FileHandler(log_path)
            fh.setFormatter(format_)
            fh.setLevel(logging.INFO)

            # 创建StreamHandler,用于输出到控制台
            ch = logging.StreamHandler()
            ch.setFormatter(format_)
            ch.setLevel(logging.INFO)

            # 添加输出
            logger.addHandler(ch)
            logger.addHandler(fh)

            # logger.removeHandler(ch)
            # logger.removeHandler(fh)
            cls.logger_instance = logger

            return cls.logger_instance


if __name__ == '__main__':
    logger = Logger().get_logger()
    logger.info('测试日志')
