# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:45
# @Author : wangjie
# @File : settings.py
# @project : SensoroApi

from common.models import Environment
from utils.jenkins_handle import ProjectName, BUILD_NUMBER, ALLURE_URL, BUILD_URL

# ------------------------------------ 通用配置 ----------------------------------------------------#
'''
开发环境：Environment.DEV
测试环境：Environment.TEST
生产环境：Environment.PROD
点军环境：Environment.DIANJUN
'''
# 设置运行环境
ENV = Environment.TEST

# 设置是否需要发送邮件：Ture发送，False不发送
IS_SEND_EMAIL = False

# 设置是否需要发送企业微信消息：Ture发送，False不发送
IS_SEND_WECHAT = False

# 设置是否开启debug日志
LOG_DEBUG = True

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

           自动化用例于 <strong>${case_start_time}</strong> 开始运行，运行时长：<strong>${case_duration}s</strong>， 目前已执行完成。<br>
           ---------------------------------------------------------------------------------------------------------------<br>
           项目名称：<strong>%s</strong> <br>
           构件编号：<strong>#%s</strong><br>
           项目环境：<strong>%s</strong><br>
           ---------------------------------------------------------------------------------------------------------------<br>
           执行结果如下:<br>
           &nbsp;&nbsp;用例运行总数:<strong> ${total_case}条</strong><br>
           &nbsp;&nbsp;通过用例数（passed）: <strong><font color="green" >${pass_case}条</font></strong><br>
           &nbsp;&nbsp;失败用例数（failed）: <strong><font color="red" >${fail_case}条</font></strong><br>
           &nbsp;&nbsp;报错用例数（error）: <strong><font color="orange" >${error_case}条</font></strong><br>
           &nbsp;&nbsp;跳过用例数（skipped）: <strong><font color="grey" >${skip_case}条</font></strong><br>
           &nbsp;&nbsp;预期失败用例数（xfail）: <strong><font color="grey" >${xfail_case}条</font></strong><br>
           &nbsp;&nbsp;预期通过用例数（xpass）: <strong><font color="grey" >${xpass_case}条</font></strong><br>
           &nbsp;&nbsp;通过率: <strong><font color="green" >${pass_rate}%%</font></strong><br>
           &nbsp;&nbsp;测试报告，点击查看: <a href='%s'>[测试报告入口]</a><br> 
           &nbsp;&nbsp;构建详情，点击查看: <a href='%s'>[控制台入口]</a><br>

           **********************************<br>
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """ % (ProjectName, BUILD_NUMBER, ENV.name, ALLURE_URL, BUILD_URL)

# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#

# 企业微信通知群聊
wechat_webhook_url = ["https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxx"]

# 企业微信通知内容
wechat_content = """******用例执行结果统计******
                > 项目名称:$%s
                > 构件编号:#%s
                > 测试环境:$%s
                > 总用例数：<font color=\"info\">${total_case}条</font>
                > 通过用例数：<font color=\"info\">${pass_case}条</font>
                > 失败用例数：<font color=\"red\">${fail_case}条</font>
                > 报错用例数：<font color=\"red\">${error_case}条</font>
                > 跳过用例数：<font color=\"warning\">${skip_case}条</font>
                > 预期失败用例数：<font color=\"comment\">${xfail_case}条</font>
                > 预期通过用例数：<font color=\"comment\">${xpass_case}条</font>
                > 通过率：<font color=\"info\">${pass_rate}%%</font>
                > 用例开始时间:<font color=\"info\">${case_start_time}</font>
                > 用例执行时长：<font color=\"info\">${case_duration}s</font>
                > 测试报告，点击查看>>[测试报告入口](%s)
                > 构建详情，点击查看>>[控制台入口](%s)
                > <@汪杰>""" % (ProjectName, BUILD_NUMBER, ENV.name, ALLURE_URL, BUILD_URL)
