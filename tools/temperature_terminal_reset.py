# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/13 16:52
# @Author : wangjie
# @File : temperature_terminal_reset.py
# @project : SensoroApi
from common.http_method import BaseApi


def temperature_terminal_reset():
    """测温终端出厂"""
    address = 'antiepidemic/v1/antiepidemic/terminal/maker'
    data = {
        'version': 'OA',
        'prefix': '测温终端',
        # 点军环境：'productId': 'bf9e0e0d-d266-11ec-be12-ee7960eede4b'
        # 生产环境：'productId': '493107a6-c168-11ec-8fd3-9eb565365869'
        # 测试环境：'productId': 'd8d151b9-bb9d-11ec-a9ee-fa2020198fdd'
        'productId': '493107a6-c168-11ec-8fd3-9eb565365869',  # 需要去物联网中台换相应环境的ID
    }
    files = [
        ('file', ('测温终端出厂.xlsx', open('/Users/wangjie/Desktop/测温终端出厂.xlsx', 'rb'),
                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    ]
    headers = {
        # 用0号商户的token
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTI1MDIxNDYxNDEwMTQ0MjU4Iiwibmlja25hbWUiOiLmsarmnbAiLCJleHAiOjE2NTYzMjIxMDEsImlhdCI6MTY1NTcxNzMwMSwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCIsInJlZnJlc2hUb2tlbiI6ImQzNDllNWUyYTEzNjQ4MWU4NzQ5NDQ5ZTQ5N2EwYmRlIiwibWVyY2hhbnRJZCI6IjAiLCJ1c2VySWQiOiIxNTI1MDIxNDYxNjI0MDUzNzYxIn0.ziWn0BmwL5OsaHCuwKsDkuCreDlSKm7IbMHUn8LTFz8-VU5baOZiVgvR8zAKhFHxxpkXFDKBVzuz6UK8VWcbag'
    }
    return BaseApi().post_(address, data=data, files=files, headers=headers)


if __name__ == '__main__':
    temperature_terminal_reset()
