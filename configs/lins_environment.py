# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:40
# @Author : wangjie
# @File : lins_environment.py
# @project : SensoroApi
from utils.command_parser import command_parser
from common.settings import ENV


class EntryPoint:
    """配置类，存放项目各个环境的默认配置"""
    _ENVIRONMENT_CONFIGS = {
        'dev': {
            'URL': "https://lins-dev1-api.sensoro.com",
            'DEFAULT_HEADERS': {},
        },
        'test': {
            'URL': "https://lins-test1-api.sensoro.com",
            'DEFAULT_HEADERS': {
                'Content-Type': 'application/json;charset=UTF-8',
                'accept-language': 'zh-CN,zh;q=0.9',
                'x-lins-view': 'all',
                'x-lins-projectid': '1622903550156582913',
                'x-lins-tenantid': '1622903542623612930',
                'x-lins-platform': 'aicity',
                # 租户为"tenantId": "1542055215455092737",
                # 'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4IiwiYXZhdGFySWQiOiIxNTQyMDU1Mjg0MDIzNTc0NTMwIiwibWVyY2hhbnRJZCI6IjE1NDIwNTUyMTU1MTM4MTI5OTMiLCJuaWNrbmFtZSI6IuaxquadsCIsInRlbmFudElkIjoiMTU0MjA1NTIxNTQ1NTA5MjczNyIsImV4cCI6MTcxMTc5MTA1NCwidXNlcklkIjoiMTU0MjA1NTI4NDAyMzU3NDUzMCIsImlhdCI6MTY4MTIwNDUwOCwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCJ9.66XK7rg6cDYMRgULdLooBWoAx2BenWkJjOt8lbqQ1LQDcmh1RlW4LsjMWUXdIhcxTQzgkvfgR1wo2QRgdK-OTg',
                # 租户为"tenantId": "1622903542623612930",
                'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4IiwiYXZhdGFySWQiOiIxNjIyOTA1ODE5MTk5NTQ5NDQxIiwibWVyY2hhbnRJZCI6IjE2MjI5MDM1NDI3Mjg0NzA1MjkiLCJuaWNrbmFtZSI6IuaxquadsCIsInRlbmFudElkIjoiMTYyMjkwMzU0MjYyMzYxMjkzMCIsImV4cCI6MTcxNTg0NjIxOSwidXNlcklkIjoiMTYyMjkwNTgxOTE5OTU0OTQ0MSIsImlhdCI6MTY4MzYxOTAxOSwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCJ9.wUV6NxBzG5dgpslNz2NUlpEehSfkbWaNMFYsYOrdO01gg4OfLbZrYOQDWdew2_LjnmORD_toPfLpL6_OawvEPg',
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
        'prod': {
            'URL': "https://lins-api.sensoro.com",
            'DEFAULT_HEADERS': {},
        },
        'dianjun': {
            'URL': "https://aicity-api.dianjun.sensoro.vip",
            'DEFAULT_HEADERS': {},
        }
    }

    # 获取命令行参数中指定的运行环境，如果没有的话就用settings中指定的环境
    args = command_parser()
    env = args.env.lower() if args.env else None

    @classmethod
    def URL(cls, env=env):
        """获取项目默认URL"""
        if env is None:
            env = ENV.value
        return cls._ENVIRONMENT_CONFIGS[env]['URL']

    @classmethod
    def DEFAULT_HEADERS(cls, env=env):
        """获取项目默认headers"""
        if env is None:
            env = ENV.value
        return cls._ENVIRONMENT_CONFIGS[env]['DEFAULT_HEADERS']

    @classmethod
    def DB_CONFIG(cls, env=env):
        """获取项目默认数据库配置"""
        if env is None:
            env = ENV.value
        return cls._ENVIRONMENT_CONFIGS[env]['DB_CONFIG']


if __name__ == '__main__':
    print(EntryPoint.URL())
    print(EntryPoint.DEFAULT_HEADERS())
