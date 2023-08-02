# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/6/2 14:44
# @Author : wangjie
# @File : config_handle.py
# @project : SensoroApi
import configparser
import os.path

from configs.dir_path_config import BASE_DIR


class CinfigHandle:
    """config文件操作"""

    def __init__(self, dir_file_name):
        """
        :param dir_file_name: 项目下文件所在目录名及文件名，如：configs/lins_environment.ini
        """
        self.file_path = os.path.join(BASE_DIR, dir_file_name)

    def get_config(self):
        """读取config配置文件"""

        config = configparser.ConfigParser()
        config.read(self.file_path, encoding="utf-8")
        return config

    def write_config(self, config, mode="a"):
        """
        将配置写入config文件，默认是追加写入
        :param config: 要写入的配置对象
        :param mode: 写入模式
        :return:
        """
        with open(self.file_path, mode=mode, encoding="utf-8") as f:
            config.write(f)


if __name__ == '__main__':
    config = CinfigHandle('configs/lins_environment.ini').get_config()
    print(config['test']['host'])

    # 读取配置
    config = CinfigHandle('configs/lins_environment.ini').get_config()
    # 修改配置项的值
    config.set("lins", "option", "new_value")
    # 写入配置
    CinfigHandle('configs/lins_environment.ini').write_config(config)
