# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:40
# @Author : wangjie
# @File : lins_environment.py
# @project : SensoroApi
from common.settings import ENV
from common.lins_environment_enums import Environment


class EntryPoint:
    _ENVIRONMENT_CONFIGS = {
        Environment.DEV: {
            'URL': "https://lins-dev1-api.sensoro.com",
            'DEFAULT_HEADERS': {},
        },
        Environment.TEST: {
            'URL': "https://lins-test1-api.sensoro.com",
            'DEFAULT_HEADERS': {
                'Content-Type': 'application/json;charset=UTF-8',
                'accept-language': 'zh-CN,zh;q=0.9',
                'x-lins-view': 'all',
                'x-lins-projectid': '1622903550156582913',
                'x-lins-tenantid': '1622903542623612930',
                'x-lins-platform': 'aicity',
                'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4IiwiYXZhdGFySWQiOiIxNTQyMDU1Mjg0MDIzNTc0NTMwIiwibWVyY2hhbnRJZCI6IjE1NDIwNTUyMTU1MTM4MTI5OTMiLCJuaWNrbmFtZSI6IuaxquadsCIsInRlbmFudElkIjoiMTU0MjA1NTIxNTQ1NTA5MjczNyIsImV4cCI6MTcxMTc5MTA1NCwidXNlcklkIjoiMTU0MjA1NTI4NDAyMzU3NDUzMCIsImlhdCI6MTY4MTIwNDUwOCwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCJ9.66XK7rg6cDYMRgULdLooBWoAx2BenWkJjOt8lbqQ1LQDcmh1RlW4LsjMWUXdIhcxTQzgkvfgR1wo2QRgdK-OTg',
            },
            'DB_CONFIG': {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': '',
                'db': 'autotest',
                'charset': 'utf8',
                # 'cursorclass': pymysql.cursors.DictCursor
            }
        },
        Environment.PROD: {
            'URL': "https://lins-api.sensoro.com",
            'DEFAULT_HEADERS': {},
        },
        Environment.DIANJUN: {
            'URL': "https://aicity-api.dianjun.sensoro.vip",
            'DEFAULT_HEADERS': {},
        }
    }

    @classmethod
    def URL(cls, env=None):
        if env is None:
            env = ENV
        return cls._ENVIRONMENT_CONFIGS[env]['URL']

    @classmethod
    def DEFAULT_HEADERS(cls, env=None):
        if env is None:
            env = ENV
        return cls._ENVIRONMENT_CONFIGS[env]['DEFAULT_HEADERS']

    @classmethod
    def DB_CONFIG(cls, env=None):
        if env is None:
            env = ENV
        return cls._ENVIRONMENT_CONFIGS[env]['DB_CONFIG']


if __name__ == '__main__':
    print(EntryPoint.URL())
    print(EntryPoint.DEFAULT_HEADERS())
