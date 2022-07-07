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
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            return otherStyleTime
        else:
            time_array = time.localtime(unix_time / 1000)
            # 转换为指定时间格式
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            return otherStyleTime

    @staticmethod
    def get_rencently_day(rencently_day=0, type='str'):
        """
        获取最近几天时间
        :param rencently_day: 几天前就减几,几天后就加几
        :param type: 默认返回字符串时间，传unix则返回时间戳
        """
        if type == 'str':
            rencently_day = ((datetime.datetime.now()) + datetime.timedelta(days=rencently_day)).strftime(
                "%Y-%m-%d %H:%M:%S")
            return rencently_day
        elif type == 'unix':
            rencently_day = ((datetime.datetime.now()) + datetime.timedelta(days=rencently_day))
            unix_time = time.mktime(rencently_day.timetuple())
            return int(round(unix_time * 1000))


if __name__ == '__main__':
    print(TimeUtil.get_current_time_str())
    print(TimeUtil.get_current_time_unix())
    print(TimeUtil.get_seven_days_ago_time_unix())
    print(TimeUtil.str_time_to_unix("2022-07-07 20:28:50"))
    print(TimeUtil.unix_time_to_str(1657197749260))
    print(TimeUtil.get_rencently_day(+8, 'unix'))
