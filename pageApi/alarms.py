# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/20 20:46
# @Author : wangjie
# @File : alarms.py
# @project : SensoroApi

from common.base_api import BaseApi


class Alarms(BaseApi):
    """预警相关接口"""

    def get_alarms_list(self, headers=None, params=None):
        """获取预警列表"""
        address = '/alarm/v1/alarms'
        headers = headers
        params = params
        return self.get(address, params=params, headers=headers)

    def get_alarms_details(self, alarms_id, headers=None, params=None):
        """获取预警详情"""
        address = f'/alarm/v1/alarms/{alarms_id}'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)


if __name__ == '__main__':
    # r = Alarms().get_alarms_list()
    r1 = Alarms().get_alarms_details('df1ddb1b-d423-11ed-a8cd-5a890753c7b1')
    print(r1.request.headers)
    print(r1.json())
