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

    def get_alarms_details(self, alarm_id, headers=None, params=None):
        """获取预警详情"""
        address = f'/alarm/v1/alarms/{alarm_id}'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def operate_alarms(self, alarm_id, headers=None, json=None):
        """操作预警"""
        address = f'/alarm/v1/alarms/{alarm_id}/operate'
        headers = headers
        json = json
        return self.put(address, headers=headers, json=json)

    def get_alarms_timeline(self, alarm_id, headers=None, params=None):
        """获取预警时间线"""
        address = f'/alarm/v1/alarms/{alarm_id}/timeline'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_config(self, headers=None, params=None):
        """获取预警相关配置"""
        address = '/alarm/v1/alarms/config'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_personCapture(self, alarm_id, headers=None, params=None):
        """获取预警相关抓拍人员"""
        address = f'/alarm/v1/alarms/{alarm_id}/personCapture'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_captureVideo(self, alarm_id, headers=None, params=None):
        """获取预警相关抓拍录像"""
        address = f'/alarm/v1/alarms/{alarm_id}/captureVideo'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_cameras(self, alarm_id, headers=None, params=None):
        """获取预警相关摄像机列表和抓拍"""
        address = f'/alarm/v1/alarms/{alarm_id}/cameras'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_actionTypes(self, headers=None, params=None):
        """获取商户所产生的所有预警类型"""
        address = '/alarm/v1/alarms/actionTypes'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_config_rules(self, headers=None, params=None):
        """获取预警事件规则列表"""
        address = '/alarm/v1/alarms/config/rules'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def put_alarms_config_rules(self, headers=None, json=None):
        """预警事件规则修改"""  # 该接口不通，接口文档也没有备注
        address = '/alarm/v1/alarms/config/rulese'
        headers = headers
        json = json
        return self.put(address, headers=headers, json=json)

    def get_alarms_devices(self, alarm_id, headers=None, params=None):
        """获取预警相关设备"""
        address = f'/alarm/v1/alarms/{alarm_id}/devices'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def get_alarms_spaces(self, alarm_id, headers=None, params=None):
        """获取预警相关空间"""
        address = f'/alarm/v1/alarms/{alarm_id}/spaces'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)

    def batch_finish_alarms(self, headers=None, json=None):
        """批量完结预警"""  # 该接口不通，接口文档也没有备注
        address = '/alarm/v1/alarms/finish/batch'
        headers = headers
        json = json
        return self.post(address, headers=headers, json=json)

    def get_alarms_tenant(self, headers=None, params=None):
        """获取预警租户列表"""
        address = '/alarm/v1/alarms/tenant/list'
        headers = headers
        params = params
        return self.get(address, headers=headers, params=params)


if __name__ == '__main__':
    # r = Alarms().get_alarms_list()
    r1 = Alarms().get_alarms_details('df1ddb1b-d423-11ed-a8cd-5a890753c7b1')
    print(r1.request.headers)
    print(r1.json())
