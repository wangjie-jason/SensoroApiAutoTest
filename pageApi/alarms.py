# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/20 20:46
# @Author : wangjie
# @File : alarms.py
# @project : SensoroApi
import time

from common.http_method import BaseApi
from utils.time_utils import TimeUtil


class Alarms(BaseApi):
    """预警相关接口"""

    def get_alarms_list(self, token, merchant_id, project_id, page=1, size=20,
                        startTime=TimeUtil.get_current_time_unix(),
                        endTime=TimeUtil.get_seven_days_ago_time_unix()):
        """获取预警列表"""
        address = 'alarm/v1/alarms'
        headers = {
            'Authorization': f'Bearer {token}',
            'X-LINS-MERCHANTID': merchant_id,
            'X-LINS-PROJECTID': project_id,
            'Accept-Language': 'zh-CN'
        }
        params = {
            'page': page,
            'size': size,
            'startTime': startTime,
            'endTime': endTime
        }
        return self.get_(address, params=params, headers=headers)


if __name__ == '__main__':
    r=Alarms().get_alarms_list(
        'eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4Iiwibmlja25hbWUiOiLmsarmnbAiLCJleHAiOjE2NTc4MDAzMTIsImlhdCI6MTY1NzE5NTUxMiwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCIsInJlZnJlc2hUb2tlbiI6IjhlYTgxNzcyMzQ5YzRlZDI5OGQ4MDAyOTg4ODNlMTEyIiwiYXZhdGFySWQiOiIxNDc5MjkyMzUyMDAzNzQzNzQ1IiwidGVuYW50SWQiOiIxNDc5MjkyMzQwNzQ2MjMxODEwIiwicHJvamVjdElkIjoiMTQ3OTI5MjM1MjQwNjM5NjkyOSIsIm1lcmNoYW50SWQiOiIxNDc5MjkyMzY2NjMzNDc2MDk3IiwidXNlcklkIjoiMTQ3OTI5MjM1MjAwMzc0Mzc0NSJ9.FDQOebUUtqkwY1DUjbUCynmHwL7fcGHbRNUtBN1ncvE7X79mYn1dDvsE8gbtzg6mHJNcsmx_t7MKsuzLdWkG3w',
        '1479292366633476097', '1479292352406396929')
    print(r.json())
