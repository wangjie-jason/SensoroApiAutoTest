# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/10 18:27
# @Author : wangjie
# @File : lock_reset.py
# @project : SensoroApi
from common.http_method import BaseApi


def lock_reset():
    """门禁出厂到测试环境"""
    address = 'enter/v1/enter/release'
    data = {
        'version': 'OA',
        'prefix': 'Test1-',
        # 生产环境：'productId': 'c14397fe-1462-11ec-a2de-0e0d1d54f276'
        # 点军环境：'productId': '26aa8aa7-d266-11ec-be12-ee7960eede4b'
        # 测试环境：'productId': '609594a2-f4fd-11eb-98f1-363f1ff6b505'
        'productId': '609594a2-f4fd-11eb-98f1-363f1ff6b505',
    }
    files = [
        ('file', ('门禁出厂.xlsx', open('/Users/wangjie/Desktop/门禁出厂.xlsx', 'rb'),
                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    ]
    headers = {
        # 用0号商户的token
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4Iiwibmlja25hbWUiOiLmsarmnbAiLCJleHAiOjE2NTU0NTQ4MDUsImlhdCI6MTY1NDg1MDAwNSwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCIsInJlZnJlc2hUb2tlbiI6ImRjNGRjZmUzYzc1NDRhMTJhNDE5ZmMzZTQyODc1ZWY3IiwibWVyY2hhbnRJZCI6IjAiLCJ1c2VySWQiOiIxNDc4MjEwNDY3MzE0MDk4MTc3In0.7lVH3UaMNqVWNDostqNrDRU-WBbyxV_8VJzodnZTL9BDPfke6ZkxlbZm5VRKuU5Wft0eQJU7ZrpGATkFupqopQ'
    }
    return BaseApi().post_(address, data=data, files=files, headers=headers)


if __name__ == '__main__':
    lock_reset()
