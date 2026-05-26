#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author : wangjie
# @File : conftest.py
# @project : SensoroApiAutoTest
import pytest

from core.http_client import HttpClient
from apis.user_api import UserApi
from utils.cache_util import CacheUtil


@pytest.fixture(scope="session")
def cache_handler() -> CacheUtil:
    """缓存管理器 fixture，注入共享数据字典"""
    return CacheUtil()


@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """session 级别的 HTTP 客户端"""
    return HttpClient()


@pytest.fixture(scope="session")
def user_api(http_client: HttpClient) -> UserApi:
    """用户接口对象"""
    return UserApi(http_client)
