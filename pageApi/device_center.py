# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/5/9 15:40
# @Author : wangjie
# @File : device_center.py
# @project : SensoroApi

from common.http_method import BaseApi


class DeviceCenter(BaseApi):
    """设备中心相关接口"""

    def get_devices_list(self, headers=None, params=None):
        """获取设备列表"""

        address = '/device/v1/deviceCenter/devices'
        headers = headers
        params = params
        return self.get(address=address, headers=headers, params=params)


if __name__ == '__main__':
    params = {
        'page': 1,
        'size': 20
    }
    r = DeviceCenter().get_devices_list(params=params)
    print(BaseApi.get_json(r))