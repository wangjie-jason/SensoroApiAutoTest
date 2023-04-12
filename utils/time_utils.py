# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 19:11
# @Author : wangjie
# @File : time_utils.py
# @project : SensoroApi
import datetime
import time


class TimeUtil:

    @staticmethod
    def get_current_time_str():
        """获取当前时间字符串"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def get_current_time_unix():
        """获取当前时间的时间戳"""
        return int(round(time.time() * 1000))

    @staticmethod
    def get_seven_days_ago_time_unix():
        """获取7天前时间的时间戳"""
        return int(round(time.time() * 1000)) - 604800000

    @staticmethod
    def str_time_to_unix(str_time):
        """将字符串时间转换为时间戳"""
        # 将其转换为时间数组
        time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳
        unix_time = int(round(time.mktime(time_array) * 1000))
        return unix_time

    @staticmethod
    def unix_time_to_str(unix_time):
        """将时间戳转换为字符串时间"""
        if len(str(unix_time)) == 10:
            # 将其转换为时间数组
            time_array = time.localtime(unix_time)
            # 转换为指定时间格式
            other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            return other_style_time
        else:
            time_array = time.localtime(unix_time / 1000)
            # 转换为指定时间格式
            other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            return other_style_time

    @staticmethod
    def get_recently_day(recently_day=0, type='str'):
        """
        获取最近几天时间
        :param recently_day: 几天前就减几,几天后就加几
        :param type: 默认返回字符串时间，传unix则返回时间戳
        """
        if type == 'str':
            recently_day = ((datetime.datetime.now()) + datetime.timedelta(days=recently_day)).strftime(
                "%Y-%m-%d %H:%M:%S")
            return recently_day
        elif type == 'unix':
            recently_day = ((datetime.datetime.now()) + datetime.timedelta(days=recently_day))
            unix_time = time.mktime(recently_day.timetuple())
            return int(round(unix_time * 1000))

    @staticmethod
    def get_day_begin_unix(recently_day=0, type='unix'):
        """
        获取某天的0点0分0秒的时间戳
        :param recently_day: 几天前就减几,几天后就加几
        :param type: 默认返回时间戳，传str则返回字符串时间
        """
        day = ((datetime.datetime.now()) + datetime.timedelta(days=recently_day)).strftime(
            "%Y-%m-%d")
        unit_day_start = int(round(time.mktime(time.strptime(day, "%Y-%m-%d")) * 1000))
        if type == 'unix':
            return unit_day_start
        elif type == 'str':
            return TimeUtil.unix_time_to_str(unit_day_start)

    @staticmethod
    def get_day_end_unix(recently_day=0, type='unix'):
        """
        获取某天的23点59分59秒的时间戳
        :param recently_day: 几天前就减几,几天后就加几
        :param type: 默认返回时间戳，传str则返回字符串时间
        """
        day = ((datetime.datetime.now()) + datetime.timedelta(days=recently_day)).strftime(
            "%Y-%m-%d")
        unit_day_end = int(round(time.mktime(time.strptime(day, "%Y-%m-%d")) * 1000 + 86399000))
        if type == 'unix':
            return unit_day_end
        elif type == 'str':
            return TimeUtil.unix_time_to_str(unit_day_end)

    @staticmethod
    def get_month_datetime_begin(date_time):
        """
        获取指定时间当月第一天00：00：00
        :param date_time: 传入datatime类型
        """
        return date_time.replace(date_time.year, date_time.month, 1, 0, 0, 0, 0)

    @staticmethod
    def get_month_datetime_end(date_time):
        """
        获取指定时间当月最后一天23：59：59
        :param date_time: 传入datatime类型
        """
        next_month = date_time.replace(date_time.year, date_time.month, 28, 23, 59, 59, 999999) + datetime.timedelta(
            days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    @staticmethod
    def compare_time(date_time1, date_time2):
        """
        比较时间大小
        :param date_time1: 传入datatime类型
        :param date_time2: 传入datatime类型
        :return: 布尔值
        """
        date_time1 = date_time1.replace()
        date_time2 = date_time2.replace()
        return date_time1 > date_time2


if __name__ == '__main__':
    print(TimeUtil.get_current_time_str())
    print(TimeUtil.get_current_time_unix())
    print(TimeUtil.get_seven_days_ago_time_unix())
    print(TimeUtil.str_time_to_unix("2022-07-07 20:28:50"))
    print(TimeUtil.unix_time_to_str(1657197749260))
    print(TimeUtil.get_recently_day(-7, 'unix'))
    print(TimeUtil.get_day_begin_unix())
    print(TimeUtil.get_day_end_unix(-4))
    print(TimeUtil.get_month_datetime_begin(datetime.datetime.now()))
    print(TimeUtil.get_month_datetime_end(datetime.datetime.now()))
    print(TimeUtil.compare_time(datetime.datetime.fromisoformat('2022-07-01 00:00:00'),
                                datetime.datetime.fromisoformat('2022-05-31 23:59:59')))
