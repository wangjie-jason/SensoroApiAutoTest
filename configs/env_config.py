# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:40
# @Author : wangjie
# @File : env_config.py
# @project : SensoroApi
import inspect

from common.settings import ENV


class DevConfig:
    """开发环境配置"""
    URL = "https://dev.com"
    DEFAULT_HEADERS = {}


class TestConfig:
    """测试环境配置"""
    URL = "https://www.wanandroid.com"
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json;charset=UTF-8',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4IiwiYXZhdGFySWQiOiIxNjIyOTA1ODE5MTk5NTQ5NDQxIiwibWVyY2hhbnRJZCI6IjE2MjI5MDM1NDI3Mjg0NzA1MjkiLCJuaWNrbmFtZSI6IuaxquadsCIsInRlbmFudElkIjoiMTYyMjkwMzU0MjYyMzYxMjkzMCIsImV4cCI6MTcxNTg0NjIxOSwidXNlcklkIjoiMTYyMjkwNTgxOTE5OTU0OTQ0MSIsImlhdCI6MTY4MzYxOTAxOSwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCJ9.wUV6NxBzG5dgpslNz2NUlpEehSfkbWaNMFYsYOrdO01gg4OfLbZrYOQDWdew2_LjnmORD_toPfLpL6_OawvEPg',
    }
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'autotest',
        'charset': 'utf8',
        # 'cursorclass': pymysql.cursors.DictCursor  # 使返回的数据格式为字典类型
    }


class ProdConfig:
    """生产环境配置"""
    URL = ""
    DEFAULT_HEADERS = {}


class EnvConfig:
    """环境配置入口"""

    # 获取settings中指定的运行环境
    _ENV = ENV

    # 缓存 _ENV_CONFIGS 字典
    _ENV_CONFIGS = None

    @classmethod
    def _generate_env_configs(cls):
        """自动匹配并生成环境配置字典"""
        if cls._ENV_CONFIGS is None:  # 只在第一次访问时生成
            cls._ENV_CONFIGS = {}
            for name, obj in globals().items():
                if inspect.isclass(obj) and name.endswith('Config') and name != 'EnvConfig':
                    env_name = name.upper().replace('CONFIG', '')  # 自动获取环境名称（例如 DevConfig -> DEV）
                    cls._ENV_CONFIGS[env_name] = obj
        return cls._ENV_CONFIGS

    @classmethod
    def get_config(cls):
        """获取指定环境的配置"""
        cls._generate_env_configs()  # 确保在第一次访问时生成配置字典
        if cls._ENV not in cls._ENV_CONFIGS:
            raise ValueError(
                f'运行的环境 "{cls._ENV}" 不存在，请检查运行的环境参数，目前支持的环境有：{", ".join(cls._ENV_CONFIGS.keys())}'
            )
        return cls._ENV_CONFIGS.get(cls._ENV)

    @classmethod
    def URL(cls):
        """获取项目默认URL"""
        return cls.get_config().URL

    @classmethod
    def DEFAULT_HEADERS(cls):
        """获取项目默认headers"""
        return cls.get_config().DEFAULT_HEADERS

    @classmethod
    def DB_CONFIG(cls):
        """获取项目默认数据库配置"""
        return cls.get_config().DB_CONFIG


if __name__ == '__main__':
    print(EnvConfig._generate_env_configs())
    print(EnvConfig.URL())
    print(EnvConfig.DEFAULT_HEADERS())
