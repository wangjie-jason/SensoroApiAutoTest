#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 19:11
# @Author : wangjie
# @File : time_util.py
# @project : SensoroApiAutoTest
"""时间工具类"""
from datetime import datetime, timedelta


class TimeUtil:
    """时间处理工具"""

    @staticmethod
    def current_str(fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
        """获取当前时间字符串"""
        return datetime.now().strftime(fmt)

    @staticmethod
    def current_unix() -> int:
        """获取当前时间的毫秒级时间戳"""
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def seven_days_ago_unix() -> int:
        """获取7天前的毫秒级时间戳"""
        dt = datetime.now() - timedelta(days=7)
        return int(dt.timestamp() * 1000)

    @staticmethod
    def str_to_unix(time_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> int:
        """字符串转Unix毫秒时间戳"""
        return int(datetime.strptime(time_str, fmt).timestamp() * 1000)

    @staticmethod
    def unix_to_str(unix_time: int, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
        """Unix毫秒时间戳转字符串"""
        if unix_time > 10 ** 12:
            unix_time = unix_time / 1000
        return datetime.fromtimestamp(unix_time).strftime(fmt)

    @staticmethod
    def recently_day(days: int, fmt: str = '%Y-%m-%d') -> str:
        """获取N天前/后的日期字符串"""
        dt = datetime.now() + timedelta(days=days)
        return dt.strftime(fmt)

    @staticmethod
    def day_begin_unix(days: int = 0) -> int:
        """获取指定天数前的当天0点毫秒时间戳，days=0表示今天"""
        dt = datetime.now() - timedelta(days=days)
        return int(dt.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)

    @staticmethod
    def day_end_unix(days: int = 0) -> int:
        """获取指定天数前的当天23:59:59毫秒时间戳"""
        dt = datetime.now() - timedelta(days=days)
        return int(dt.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp() * 1000)

    @staticmethod
    def month_begin(dt: datetime = None) -> int:
        """获取当月1号0点的毫秒时间戳"""
        dt = dt or datetime.now()
        first_day = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return int(first_day.timestamp() * 1000)

    @staticmethod
    def month_end(dt: datetime = None) -> int:
        """获取当月最后一天23:59:59的毫秒时间戳"""
        dt = dt or datetime.now()
        next_month = dt.replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        last_day = last_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        return int(last_day.timestamp() * 1000)

    @staticmethod
    def compare_time(date_time1, date_time2):
        """
        比较时间大小
        :param date_time1: 传入datatime类型
        :param date_time2: 传入datatime类型
        :return: 布尔值
        """
        return date_time1 > date_time2


if __name__ == '__main__':
    print(TimeUtil.current_str())
    print(TimeUtil.current_unix())
    print(TimeUtil.seven_days_ago_unix())
    print(TimeUtil.str_to_unix("2022-07-07 20:28:50"))
    print(TimeUtil.unix_to_str(1657197749260))
    print(TimeUtil.recently_day(-7))
    print(TimeUtil.day_begin_unix())
    print(TimeUtil.day_end_unix(-4))
    print(TimeUtil.month_begin(datetime.now()))
    print(TimeUtil.month_end(datetime.now()))
    print(TimeUtil.compare_time(datetime.fromisoformat('2022-07-01 00:00:00'),
                                datetime.fromisoformat('2022-05-31 23:59:59')))
