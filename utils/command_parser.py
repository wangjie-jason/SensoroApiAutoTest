# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/6/21 20:24
# @Author : wangjie
# @File : command_parser.py
# @project : SensoroApi


import argparse


def command_parser():
    """ 解析指定的命令行参数 """
    # 创建解析器对象
    parser = argparse.ArgumentParser()

    # 添加命令行参数选项
    parser.add_argument('-w', '--send-wechat', choices=['False', 'True'], type=str, default=None,
                        help='指定是否需要发送企业微信群消息')
    parser.add_argument('-e', '--send-email', choices=['False', 'True'], type=str, default=None,
                        help='指定是否需要发送邮件')
    parser.add_argument('-env', '--env', choices=['DEV', 'TEST', 'PROD'], type=lambda s: s.upper(), default=None,
                        help='指定运行环境,并支持大小输入')

    # 解析命令行参数
    args, unknown_args = parser.parse_known_args()

    return args


if __name__ == '__main__':
    args = command_parser()
    # 获取命令行参数的值并赋值给对应的变量
    IS_SEND_WECHAT = eval(args.send_wechat) if args.send_wechat else None
    IS_SEND_EMAIL = eval(args.send_email) if args.send_email else None
    ENV = args.env

    # 打印变量的值
    print('IS_SEND_WECHAT:', IS_SEND_WECHAT)
    print('IS_SEND_EMAIL:', IS_SEND_EMAIL)
    print('ENV:', ENV)
