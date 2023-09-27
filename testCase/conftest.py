# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/5/24 18:11
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApi
import pytest

from common.base_api import BaseApi
from common.base_log import logger
from pageApi.login import Login
from utils.cache_handle import CacheHandler


@pytest.fixture(scope="session", autouse=False)
def get_token():
    """获取登录V1的token"""
    logger.info("开始用例前置操作")
    # 调登录接口，获取登录接口的token¬
    login_response = Login().login('18800000001', '123456')
    token = BaseApi.get_json(login_response)['data']['token']
    CacheHandler.set_cache('Authorization', f'Bearer {token}')
    logger.info("结束用例前置操作")
    return token
