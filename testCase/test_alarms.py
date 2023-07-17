# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/20 21:18
# @Author : wangjie
# @File : test_alarms.py
# @project : SensoroApi
import allure
import pytest

from common.base_api import BaseApi
from pageApi.alarms import Alarms
from utils.time_utils import TimeUtil


@allure.epic("预警模块")
@allure.feature("事件中心预警模块")
class TestAlarms:
    """测试预警"""

    @allure.story('事件中心')
    @allure.title('获取预警列表')
    # @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    def test_get_alarms_list(self, get_token_v2, set_global_data):
        """获取预警列表"""
        headers = {'Authorization': f'Bearer {get_token_v2}'}
        params = {
            'page': 1,
            'size': 20,
            'startTime': TimeUtil.get_current_time_unix(),
            'endTime': TimeUtil.get_seven_days_ago_time_unix()
        }
        r = Alarms().get_alarms_list(headers=headers, params=params)
        alarm_id = BaseApi.get_json(r)['data']['list'][0]['id']
        set_global_data('alarm_id', alarm_id)
        message = BaseApi.get_json(r)['message']
        assert message == 'SUCCESS'

    @allure.story('事件中心')
    @allure.title('获取预警详情')
    @pytest.mark.dependency(depends=["TestAlarms::test_get_alarms_list"])
    def test_get_alarms_details(self, get_token_v2, get_global_data):
        """获取预警详情"""
        headers = {'Authorization': f'Bearer {get_token_v2}'}
        alarm_id = get_global_data('alarm_id')
        print('取出来的alarms_id：', alarm_id)
        r = Alarms().get_alarms_details(alarm_id, headers=headers)
        message = BaseApi.get_json(r)['message']
        assert message == 'SUCCESS'
