# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/20 21:18
# @Author : wangjie
# @File : test_alarms.py
# @project : SensoroApi
from time import sleep

from page_api.alarms import Alarms


class TestAlarms:
    """测试预警"""

    def test_get_alarms_list(self, get_token_v2):
        """获取预警列表"""
        r = Alarms().get_alarms_list(token=get_token_v2, merchant_id='1479292366633476097',
                                     project_id='1479292352406396929')
        assert r['message'] == 'SUCCESS'
