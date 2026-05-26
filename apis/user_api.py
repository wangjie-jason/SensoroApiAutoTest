#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author : wangjie
# @File : user_api.py
# @project : SensoroApiAutoTest
"""用户模块 API 接口（PO模式，基于 JSONPlaceholder 示例）"""
from pydantic import BaseModel, ConfigDict, Field
from requests import Response

from core.http_client import HttpClient


class CreatePostParams(BaseModel):
    """创建帖子请求参数"""
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., description="帖子标题")
    body: str = Field(..., description="帖子内容")
    userId: int = Field(..., description="用户ID")


class UserApi:
    """用户模块接口封装"""

    def __init__(self, client: HttpClient):
        self._client = client

    def get_users(self, headers: dict = None) -> Response:
        """获取用户列表"""
        return self._client.get('/users', headers=headers)

    def get_user(self, user_id: int, headers: dict = None) -> Response:
        """获取指定用户详情"""
        return self._client.get(f'/users/{user_id}', headers=headers)

    def create_post(self, title: str, body: str, user_id: int, headers: dict = None) -> Response:
        """创建帖子"""
        params = CreatePostParams(title=title, body=body, userId=user_id)
        return self._client.post('/posts', json_data=params.model_dump(), headers=headers)


if __name__ == '__main__':
    client = HttpClient()
    api = UserApi(client)

    r = api.get_users()
    print(HttpClient.get_json(r))
