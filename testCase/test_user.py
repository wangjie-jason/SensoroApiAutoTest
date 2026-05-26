#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author : wangjie
# @File : test_user.py
# @project : SensoroApiAutoTest
import os

import allure
import pytest

from core.http_client import HttpClient
from core.paths import DATAS_DIR
from apis.user_api import UserApi
from utils.yaml_util import YamlUtil


@allure.feature("用户模块")
class TestUser:
    """测试用户相关接口（基于 JSONPlaceholder 示例 API）"""

    # 加载测试数据
    data_user = YamlUtil.read_yaml(DATAS_DIR / 'user.yaml')
    params_user = [(item['case_title'], item.get('user_id'), item.get('expected_name'),
                    item.get('expected_status')) for item in data_user]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("测试获取用户列表")
    @allure.title("获取所有用户")
    @pytest.mark.run(order=1)
    def test_get_users(self, user_api: UserApi, http_client: HttpClient):
        """获取用户列表，验证返回数据"""
        with allure.step("发送获取用户列表请求"):
            response = user_api.get_users()

        with allure.step("验证响应结果"):
            response_data = http_client.get_json(response)
            assert http_client.get_status_code(response) == 200
            assert isinstance(response_data, list)
            assert len(response_data) == 10

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("测试获取用户详情")
    @allure.title('{case_title}')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('case_title, user_id, expected_name, expected_status', params_user)
    def test_get_user(self, case_title, user_id, expected_name, expected_status,
                      user_api: UserApi, http_client: HttpClient):
        """获取指定用户详情"""
        with allure.step("发送获取用户详情请求"):
            response = user_api.get_user(user_id)

        with allure.step("验证响应结果"):
            status_code = http_client.get_status_code(response)

            if expected_status:
                assert status_code == expected_status
            else:
                assert status_code == 200
                response_data = http_client.get_json(response)
                assert response_data['name'] == expected_name

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("测试创建帖子")
    @allure.title("创建帖子")
    @pytest.mark.run(order=3)
    def test_create_post(self, user_api: UserApi, http_client: HttpClient):
        """创建一篇新帖子"""
        with allure.step("发送创建帖子请求"):
            response = user_api.create_post(
                title="Test Post Title",
                body="This is a test post body.",
                user_id=1
            )

        with allure.step("验证响应结果"):
            assert http_client.get_status_code(response) == 201
            response_data = http_client.get_json(response)
            assert response_data['title'] == "Test Post Title"
            assert response_data['body'] == "This is a test post body."
            assert response_data['userId'] == 1
            assert 'id' in response_data
