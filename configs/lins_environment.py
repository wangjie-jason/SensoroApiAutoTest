# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:40
# @Author : wangjie
# @File : lins_environment.py
# @project : SensoroApi
from common.settings import ENV
from configs.lins_environment_enum import Environment


class EntryPoint:
    _ENV_URL = {
        Environment.DEV: "https://lins-dev1-api.sensoro.com/",
        Environment.TEST: "https://lins-test1-api.sensoro.com/",
        Environment.PROD: "https://lins-api.sensoro.com/",
        Environment.DIANJUN: "https://aicity-api.dianjun.sensoro.vip/"
    }

    @property
    def URL(self):
        return self._ENV_URL[ENV]


if __name__ == '__main__':
    print(EntryPoint().URL)
