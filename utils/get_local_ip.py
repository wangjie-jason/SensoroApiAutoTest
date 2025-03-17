#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/7 14:48
# @Author : wangjie
# @File : get_local_ip.py
# @project : SensoroApi


import socket


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    finally:
        _s.close()

    return l_host
if __name__ == '__main__':
    print(get_host_ip())
