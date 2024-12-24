# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:45
# @Author : wangjie
# @File : settings.py
# @project : SensoroApi

from utils.command_parser import command_parser
from utils.jenkins_handle import ProjectName, BUILD_NUMBER, ALLURE_URL, BUILD_URL

# ------------------------------------ 通用配置 ----------------------------------------------------#
# 获取命令行参数
args = command_parser()

# 设置默认运行环境，如果命令行中有 env 参数并且有效，使用命令行的值，否则使用默认值，支持的环境参考env_config中配置的环境
ENV = (args.env or "dev").upper()

# 失败重跑次数
rerun = 0

# 失败重跑间隔时间
reruns_delay = 5

# 当用例达到最大失败数，整个测试停止执行
max_fail = 100

# 设置是否需要发送邮件：Ture发送，False不发送，如果命令行中有 send_email 参数并且有效，使用命令行的值，否则使用else后的默认值
IS_SEND_EMAIL = args.send_email == 'true' if args.send_email else False

# 设置是否需要发送企业微信消息：Ture发送，False不发送，如果命令行中有 send_wechat 参数并且有效，使用命令行的值，否则使用else后的默认值
IS_SEND_WECHAT = args.send_wechat == 'true' if args.send_wechat else False

# 设置是否开启debug日志
LOG_DEBUG = False

# 设置是否开启控制台日志
LOG_CONSOLE = True

# ------------------------------------ 邮件配置信息 ----------------------------------------------------#

# 发送邮件配置信息
email_config = {
    'mail_subject': '接口自动化测试报告',  # 邮件标题
    'sender_username': 'xxxxx@qq.com',  # 发件人邮箱
    'sender_password': 'ASDsdasda',  # 发件人邮箱授权码
    'receiver_mail_list': ['xxxxx@qq.com', ],  # 收件人邮箱
    'smtp_domain': 'smtp.exmail.qq.com',  # 发送邮箱的域名
    'smtp_port': 465,  # 发送邮箱的端口号
}

# 邮件通知内容
email_content = """
           各位同事, 大家好:<br>

           自动化用例于 <strong>${start_time}</strong> 开始运行，运行时长：<strong>${duration}s</strong>， 目前已执行完成。<br>
           --------------------------------------------------------------------------------------------------------<br>
           项目名称：<strong>%s</strong> <br>
           构件编号：<strong>#%s</strong><br>
           项目环境：<strong>%s</strong><br>
           --------------------------------------------------------------------------------------------------------<br>
           执行结果如下:<br>
           &nbsp;&nbsp;用例运行总数:<strong> ${total}条</strong><br>
           &nbsp;&nbsp;通过用例数（passed）: <strong><font color="green" >${passed}条</font></strong><br>
           &nbsp;&nbsp;失败用例数（failed）: <strong><font color="red" >${failed}条</font></strong><br>
           &nbsp;&nbsp;报错用例数（error）: <strong><font color="orange" >${error}条</font></strong><br>
           &nbsp;&nbsp;跳过用例数（skipped）: <strong><font color="grey" >${skipped}条</font></strong><br>
           &nbsp;&nbsp;预期失败用例数（xfailed）: <strong><font color="grey" >${xfailed}条</font></strong><br>
           &nbsp;&nbsp;预期通过用例数（xpassed）: <strong><font color="grey" >${xpassed}条</font></strong><br>
           &nbsp;&nbsp;通过率: <strong><font color="green" >${pass_rate}%%</font></strong><br>
           &nbsp;&nbsp;测试报告，点击查看: <a href='%s'>[测试报告入口]</a><br> 
           &nbsp;&nbsp;构建详情，点击查看: <a href='%s'>[控制台入口]</a><br>

           **********************************<br>
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """ % (ProjectName, BUILD_NUMBER, ENV, ALLURE_URL, BUILD_URL)

# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#

# 企业微信通知群聊
wechat_webhook_url = ["https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxx"]

# 企业微信通知内容
wechat_content = """******用例执行结果统计******
                > 项目名称:%s
                > 构件编号:#%s
                > 测试环境:%s
                > 总用例数：<font color=\"info\">${total}条</font>
                > 通过用例数：<font color=\"info\">${passed}条</font>
                > 失败用例数：<font color=\"red\">${failed}条</font>
                > 报错用例数：<font color=\"red\">${error}条</font>
                > 跳过用例数：<font color=\"warning\">${skipped}条</font>
                > 预期失败用例数：<font color=\"comment\">${xfailed}条</font>
                > 预期通过用例数：<font color=\"comment\">${xpassed}条</font>
                > 通过率：<font color=\"info\">${pass_rate}%%</font>
                > 用例开始时间:<font color=\"info\">${start_time}</font>
                > 用例执行时长：<font color=\"info\">${duration}s</font>
                > 测试报告，点击查看>>[测试报告入口](%s)
                > 构建详情，点击查看>>[控制台入口](%s)
                > <@汪杰>""" % (ProjectName, BUILD_NUMBER, ENV, ALLURE_URL, BUILD_URL)
