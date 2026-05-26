#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:40
# @Author : wangjie
# @File : config_manager.py
# @project : SensoroApiAutoTest
import os
from functools import lru_cache
from typing import Any

from core.exceptions import ConfigError
from core.paths import CONFIG_DIR
from utils.command_parser import command_parser
from utils.yaml_util import YamlUtil

# ===================== 命令行参数 =====================
args = command_parser()


# ===================== 配置管理器 =====================
class ConfigManager:
    """全局统一配置入口（合并环境 + 运行 + 通知）"""

    @classmethod
    @lru_cache(maxsize=1)
    def _raw_settings(cls) -> dict[str, Any]:
        settings_file = CONFIG_DIR / "settings.yaml"
        if not settings_file.exists():
            raise ConfigError(f"配置文件不存在：{settings_file}")
        return YamlUtil.read_yaml(settings_file)

    @classmethod
    @lru_cache(maxsize=1)
    def _raw_environments(cls) -> dict[str, Any]:
        environments_file = CONFIG_DIR / "environments.yaml"
        if not os.path.exists(environments_file):
            raise ConfigError(f"环境配置文件不存在：{environments_file}")
        return YamlUtil.read_yaml(environments_file)

    @classmethod
    def _get_available_env_names(cls) -> list[str]:
        """返回已配置的环境名称。"""
        return sorted(cls._raw_environments())

    @classmethod
    @lru_cache(maxsize=1)
    def _get_env_config(cls) -> dict[str, Any]:
        """获取指定环境的配置"""
        env = cls.current_env()
        available_envs = cls._get_available_env_names()
        if env not in available_envs:
            raise ValueError(
                f'运行的环境 "{env}" 不存在，可用环境：{", ".join(available_envs)}'
            )
        return cls._raw_environments()[env]

    # ===================== 环境配置 =====================
    @classmethod
    @lru_cache(maxsize=1)
    def current_env(cls) -> str:
        """获取当前生效环境，命令行参数优先级高于配置文件"""
        env_from_cmd = args.env
        env_from_yaml = cls._raw_settings().get('project', {}).get("default_env", "TEST")
        return (env_from_cmd or env_from_yaml).strip().upper()

    @classmethod
    def project_name(cls) -> str:
        """获取当前项目名称"""
        return cls._raw_settings().get('project', {}).get("name", "API自动化测试")

    @classmethod
    def base_url(cls) -> str:
        """获取项目默认URL"""
        return cls._get_env_config().get('base_url', '')

    @classmethod
    def default_headers(cls) -> dict:
        """获取项目默认headers"""
        return cls._get_env_config().get('default_headers', {})

    @classmethod
    def db_config(cls) -> dict:
        """获取项目默认数据库配置"""
        return cls._get_env_config().get('database', {})

    # ===================== 运行配置 =====================
    @classmethod
    def rerun_count(cls) -> int:
        """失败重跑次数"""
        return cls._raw_settings().get("runtime", {}).get("rerun_count", 2)

    @classmethod
    def rerun_delay_seconds(cls) -> int:
        """失败重跑间隔时间"""
        return cls._raw_settings().get("runtime", {}).get("rerun_delay_seconds", 5)

    @classmethod
    def max_fail_count(cls) -> int:
        """设置当本次测试流程所有失败用例达到最大失败数，停止执行"""
        return cls._raw_settings().get("runtime", {}).get("max_fail_count", 100)

    @classmethod
    def log_level(cls) -> int:
        """设置日志等级"""
        return cls._raw_settings().get("runtime", {}).get("log_level", 'INFO')

    @classmethod
    def console_log(cls) -> bool:
        """设置是否开启控制台日志"""
        return cls._raw_settings().get("runtime", {}).get("console_log", False)

    # ===================== 通知开关 =====================
    @classmethod
    def is_send_email(cls) -> bool:
        """是否发送邮件通知"""
        if args.send_email is not None:
            return args.send_email == "true"
        return cls._raw_settings().get('notifications', {}).get('email', {}).get("enabled", False)

    @classmethod
    def is_send_wechat(cls) -> bool:
        """是否发送企业微信通知"""
        if args.send_wechat is not None:
            return args.send_wechat == "true"
        return cls._raw_settings().get('notifications', {}).get('wechat', {}).get("enabled", False)

    # ===================== 邮件配置 =====================
    @classmethod
    def email_config(cls) -> dict:
        """邮箱配置"""
        return cls._raw_settings().get('notifications', {}).get('email', {}).get('email_config', {})

    @classmethod
    def email_content(cls) -> str:
        """邮箱通知模板内容"""
        return cls._raw_settings().get('notifications', {}).get('email', {}).get('content_template', "")

    # ===================== 企业微信配置 =====================
    @classmethod
    def wechat_webhook_urls(cls) -> list[str]:
        """企业微信配置"""
        return cls._raw_settings().get('notifications', {}).get("wechat", {}).get("webhook_urls", [])

    @classmethod
    def wechat_content(cls) -> str:
        """邮箱通知模板内容"""
        return cls._raw_settings().get('notifications', {}).get('wechat', {}).get('content_template', "")


# ===================== 全局唯一导出 =====================
config = ConfigManager()

if __name__ == '__main__':
    # print(EnvConfig._generate_env_configs())
    print(config.current_env())
    # print(ConfigManager._raw_environments().get('TEST'))
    # print(ConfigManager.base_url())
    # print(ConfigManager.default_headers())
