#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import pytest

if __name__ == '__main__':
    # # 执行pytest单元测试，生成 Allure原始报告需要的数据存在 /Temp 目录
    # pytest.main(['-vs', 'testCase/', '--alluredir', './Temp'])
    # # 使用allure generate -o 命令将./Temp目录下的临时报告导出到TestReport目录
    # os.system('allure generate ./Temp -o ./outFiles/report --clean')

    pytest.main()
    os.system('allure generate ./Temp -o ./outFiles/report --clean')
