#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:40
# @Author : wangjie
# @File : config_manager.py
# @project : SensoroApiAutoTest
import json
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

    # ===================== 环境变量覆盖机制 =====================
    @staticmethod
    def _env_override(env_var: str, default: Any) -> Any:
        """
        从环境变量获取配置值，不存在则返回 YAML 默认值

        - 布尔值容错：true/True/TRUE、false/False/FALSE 均识别为布尔值
        - JSON 格式的值（如列表、字典、数字）会自动解析
        - 普通字符串原样返回

        两种注入来源均可使用，代码层只认 os.environ，不区分来源：
        - K8s Secrets:      通过 Pod Template 的 envFrom.secretRef 注入
        - Jenkins 凭据:     通过 Jenkinsfile 的 withCredentials 注入

        用法：
            export EMAIL_SENDER_PASSWORD=xxx
            export WECHAT_WEBHOOK_URLS='["url1", "url2"]'
            export SEND_EMAIL=true
        """
        value = os.environ.get(env_var)
        if value is None:
            return default

        # 布尔值容错：true/false 不区分大小写
        lower_val = value.strip().lower()
        if lower_val in ('true', 'false'):
            return lower_val == 'true'

        # JSON 解析（列表、字典、数字等）
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    # ===================== 内部数据加载 =====================
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
        """返回已配置的环境名称"""
        return sorted(cls._raw_environments())

    @classmethod
    @lru_cache(maxsize=1)
    def _get_env_config(cls) -> dict[str, Any]:
        """获取当前环境的配置"""
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
        """获取当前生效环境，命令行参数优先级高于配置文件，可通过 TEST_ENV 环境变量覆盖"""
        env_from_env = os.environ.get("TEST_ENV")
        if env_from_env:
            return env_from_env.strip().upper()
        env_from_cmd = args.env
        env_from_yaml = cls._raw_settings().get('project', {}).get("default_env", "TEST")
        return (env_from_cmd or env_from_yaml).strip().upper()

    @classmethod
    def project_name(cls) -> str:
        """获取当前项目名称"""
        return cls._raw_settings().get('project', {}).get("name", "SENSORO API自动化测试")

    @classmethod
    def base_url(cls) -> str:
        """获取当前环境的 base_url，可通过 BASE_URL 环境变量覆盖"""
        default = cls._get_env_config().get('base_url', '')
        return cls._env_override('BASE_URL', default)

    @classmethod
    def default_headers(cls) -> dict:
        """获取当前环境的默认 headers，可通过 DEFAULT_HEADERS 环境变量覆盖（JSON 格式）"""
        default = cls._get_env_config().get('default_headers', {})
        headers = cls._env_override('DEFAULT_HEADERS', default)
        # AUTHORIZATION_TOKEN 环境变量优先级最高
        token = os.environ.get("AUTHORIZATION_TOKEN")
        if token:
            headers["authorization"] = token
        return headers

    @classmethod
    def db_config(cls) -> dict:
        """获取数据库配置，密码/用户名/主机可通过环境变量覆盖"""
        db = cls._get_env_config().get('database', {})
        db['host'] = cls._env_override('DB_HOST', db.get('host', ''))
        db['port'] = int(cls._env_override('DB_PORT', db.get('port', 3306)))
        db['user'] = cls._env_override('DB_USER', db.get('user', ''))
        db['password'] = cls._env_override('DB_PASSWORD', db.get('password', ''))
        db['db'] = cls._env_override('DB_NAME', db.get('db', ''))
        return db

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
        """本次测试流程所有失败用例达到最大失败数时停止执行"""
        return cls._raw_settings().get("runtime", {}).get("max_fail_count", 100)

    @classmethod
    def log_level(cls) -> str:
        """日志等级，环境变量值自动转大写"""
        default = cls._raw_settings().get("runtime", {}).get("log_level", 'INFO')
        return cls._env_override('LOG_LEVEL', default).upper()

    @classmethod
    def console_log(cls) -> bool:
        """是否开启控制台日志"""
        default = cls._raw_settings().get("runtime", {}).get("console_log", False)
        return cls._env_override('CONSOLE_LOG', default)

    # ===================== 通知开关 =====================
    @classmethod
    def is_send_email(cls) -> bool:
        """是否发送邮件通知，命令行参数 > 环境变量 > YAML 配置"""
        if args.send_email is not None:
            return args.send_email == "true"
        default = cls._raw_settings().get('notifications', {}).get('email', {}).get("enabled", False)
        return cls._env_override('SEND_EMAIL', default)

    @classmethod
    def is_send_wechat(cls) -> bool:
        """是否发送企业微信通知，命令行参数 > 环境变量 > YAML 配置"""
        if args.send_wechat is not None:
            return args.send_wechat == "true"
        default = cls._raw_settings().get('notifications', {}).get('wechat', {}).get("enabled", False)
        return cls._env_override('SEND_WECHAT', default)

    # ===================== 邮件配置 =====================
    @classmethod
    def email_config(cls) -> dict:
        """邮箱配置，密码/用户名等可通过环境变量覆盖"""
        cfg = cls._raw_settings().get('notifications', {}).get('email', {}).get('email_config', {})
        cfg['mail_subject'] = cls._env_override('EMAIL_SUBJECT', cfg.get('mail_subject', ''))
        cfg['sender_username'] = cls._env_override('EMAIL_SENDER_USERNAME', cfg.get('sender_username', ''))
        cfg['sender_password'] = cls._env_override('EMAIL_SENDER_PASSWORD', cfg.get('sender_password', ''))
        cfg['receiver_mail_list'] = cls._env_override('EMAIL_RECEIVERS', cfg.get('receiver_mail_list', []))
        cfg['smtp_domain'] = cls._env_override('SMTP_DOMAIN', cfg.get('smtp_domain', ''))
        cfg['smtp_port'] = int(cls._env_override('SMTP_PORT', cfg.get('smtp_port', 465)))
        return cfg

    @classmethod
    def email_content(cls) -> str:
        """邮件通知模板内容"""
        return cls._raw_settings().get('notifications', {}).get('email', {}).get('content_template', "")

    # ===================== 企业微信配置 =====================
    @classmethod
    def wechat_webhook_urls(cls) -> list[str]:
        """企业微信 webhook 地址列表，可通过 WECHAT_WEBHOOK_URLS 环境变量覆盖（JSON 数组格式）"""
        default = cls._raw_settings().get('notifications', {}).get("wechat", {}).get("webhook_urls", [])
        return cls._env_override('WECHAT_WEBHOOK_URLS', default)

    @classmethod
    def wechat_content(cls) -> str:
        """企业微信通知模板内容"""
        return cls._raw_settings().get('notifications', {}).get('wechat', {}).get('content_template', "")


# ===================== 全局唯一导出 =====================
config = ConfigManager()

if __name__ == '__main__':
    print(config.current_env())
