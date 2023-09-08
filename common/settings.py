# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/7/7 11:45
# @Author : wangjie
# @File : settings.py
# @project : SensoroApi

from common.models import Environment
from utils.jenkins_handle import ProjectName, BUILD_NUMBER, ALLURE_URL, BUILD_URL
from utils.reportdatahandle import ReportDataHandle

# 设置运行的环境变量
'''
开发环境：Environment.DEV
测试环境：Environment.TEST
生产环境：Environment.PROD
点军环境：Environment.DIANJUN
'''
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

# 发送邮件的相关配置信息
email_config = {
    'mail_subject': '接口自动化测试报告',  # 邮件标题
    'sender_username': 'xxxxx@qq.com',  # 发件人邮箱
    'sender_password': 'ASDsdasda',  # 发件人邮箱授权码
    'receiver_mail_list': ['xxxxx@qq.com', ],  # 收件人邮箱
    'smtp_domain': 'smtp.exmail.qq.com',  # 发送邮箱的域名
    'smtp_port': 465,  # 发送邮箱的端口号
}

# TODO:使用模板替换的方式替换该部分内容，否则此处会读取上次执行的报告
# 邮件通知内容
pytest_result = ReportDataHandle.pytest_json_report_case_count()
email_content = f"""
           各位同事, 大家好:<br>

           自动化用例于 <strong>{pytest_result["case_start_time"]}</strong> 开始运行，运行时长：<strong>{pytest_result['case_duration']}s</strong>， 目前已执行完成。<br>
           ---------------------------------------------------------------------------------------------------------------<br>
           项目名称：<strong>{ProjectName}</strong> <br>
           构件编号：<strong>#{BUILD_NUMBER}</strong><br>
           项目环境：<strong>{ENV.name}</strong><br>
           ---------------------------------------------------------------------------------------------------------------<br>
           执行结果如下:<br>
           &nbsp;&nbsp;用例运行总数:<strong> {pytest_result['total_case']}条</strong><br>
           &nbsp;&nbsp;通过用例个数（passed）: <strong><font color="green" >{pytest_result['pass_case']}条</font></strong><br>
           &nbsp;&nbsp;失败用例个数（failed）: <strong><font color="red" >{pytest_result['fail_case']}条</font></strong><br>
           &nbsp;&nbsp;报错用例个数（error）: <strong><font color="orange" >{pytest_result['error_case']}条</font></strong><br>
           &nbsp;&nbsp;跳过用例个数（skipped）: <strong><font color="grey" >{pytest_result['skip_case']}条</font></strong><br>
           &nbsp;&nbsp;预期失败用例个数（xfail）: <strong><font color="grey" >{pytest_result['xfail_case']}条</font></strong><br>
           &nbsp;&nbsp;预期通过用例个数（xpass）: <strong><font color="grey" >{pytest_result['xpass_case']}条</font></strong><br>
           &nbsp;&nbsp;通过率: <strong><font color="green" >{pytest_result['pass_rate']}%</font></strong><br>
           &nbsp;&nbsp;测试报告，点击查看: <a href='{ALLURE_URL}'>[测试报告入口]</a><br> 
           &nbsp;&nbsp;构建详情，点击查看: <a href='{BUILD_URL}'>[控制台入口]</a><br>

           **********************************<br>
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """

# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#
# 企业微信通知群聊
wechat_webhook_url = ["https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxx"]

# 企业微信通知内容
wechat_content = f"""******用例执行结果统计******
                > 项目名称:{ProjectName}
                > 构件编号:#{BUILD_NUMBER}
                > 测试环境:{ENV.name}
                > 总用例数：<font color=\"info\">{pytest_result['total_case']}条</font>
                > 通过用例数：<font color=\"info\">{pytest_result['pass_case']}条</font>
                > 失败用例数：<font color=\"red\">{pytest_result['fail_case']}条</font>
                > 报错用例数：<font color=\"red\">{pytest_result['error_case']}条</font>
                > 跳过用例数：<font color=\"warning\">{pytest_result['skip_case']}条</font>
                > 预期失败用例数：<font color=\"comment\">{pytest_result['xfail_case']}条</font>
                > 预期通过用例数：<font color=\"comment\">{pytest_result['xpass_case']}条</font>
                > 通过率：<font color=\"info\">{pytest_result['pass_rate']}%</font>
                > 用例开始时间:<font color=\"info\">{pytest_result["case_start_time"]}</font>
                > 用例执行时长：<font color=\"info\">{pytest_result['case_duration']}s</font>
                > 测试报告，点击查看>>[测试报告入口]({ALLURE_URL})
                > 构建详情，点击查看>>[控制台入口]({BUILD_URL})
                > <@汪杰>"""
