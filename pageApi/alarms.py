# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/20 20:46
# @Author : wangjie
# @File : alarms.py
# @project : SensoroApi
import time

from common.http_method import BaseApi


class Alarms(BaseApi):
    """预警相关接口"""

    def get_alarms_list(self, token, merchant_id, project_id, page=1, size=20, startTime=int(round(time.time() * 1000)),
                        endTime=int(round(time.time() * 1000)) - 604800000):
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
    Alarms().get_alarms_list(
        'eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4Iiwibmlja25hbWUiOiLmsarmnbAiLCJleHAiOjE2NTYzODgyMDIsImlhdCI6MTY1NTc4MzQwMiwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCIsInJlZnJlc2hUb2tlbiI6IjA3OWEyMTU5MWVlYTRmMTA4MDI1OWUzNWI0OTdlYjQ0IiwiYXZhdGFySWQiOiIxNDc5MjkyMzUyMDAzNzQzNzQ1IiwidGVuYW50SWQiOiIxNDc5MjkyMzQwNzQ2MjMxODEwIiwicHJvamVjdElkIjoiMTQ3OTI5MjM1MjQwNjM5NjkyOSIsIm1lcmNoYW50SWQiOiIxNDc5MjkyMzY2NjMzNDc2MDk3IiwidXNlcklkIjoiMTQ3OTI5MjM1MjAwMzc0Mzc0NSJ9.WFAVSBy2oxd6N3Rf5WQfaKmMofbfu37UP7BzTkE7FkQhcDhos8ugKYtHiDtMc4MUPO9UWqbsFNrzR83mk5Fkew',
        '1479292366633476097', '1479292352406396929')
