# SensoroApi

## 准备Python环境

- 安装Python>=3.6
- 安装依赖 
    - pip3 install -r requirements.txt

## 项目结构
```

├── README.md                                     	项目说明文件
├── Temp						allure报告临时存放目录
├── common						公共方法类存放目录
│     ├── base_log.py					日志记录器
│     ├── base_api.py				        基础类，对请求方法进行二次封装
│     ├── lins_environment_enums.py			项目环境枚举
│     ├── mail_sender.py				发送邮件方法
│     └── settings.py					项目配置文件
├── configs						项目配置信息目录
│     ├── dir_path_config.py				项目各目录路径文件
│     ├── lins_environment.ini				项目全局环境变量配置文件（弃用）
│     ├── lins_environment.py				项目全局环境变量
│     └── mail_config.yaml				发送邮件配置信息
├── conftest.py						pytest共享文件，设置allure报告及其他报告的环境变量
├── datas						测试数据存放目录
│     ├── login.yaml					登录测试的数据demo
├── environment.properties				allure报告环境变量展示文件
├── outFiles						各种输出文件存放目录
│     ├── logs						日志存放目录
│     ├── pytest_report					pytest报告存放目录
│     ├── report					allure报告存放目录 
│     └── screenShot					截图存放目录
├── pageApi						各业务接口对象类
│     ├── alarms.py					预警相关接口demo
│     └── login.py					登录相关接口demo
├── pytest.ini						pytest启动项配置文件
├── requirements.txt					python项目依赖文件
├── run.py						执行测试用例主入口
├── testCase						测试用例存放目录
│     ├── conftest.py					pytest共享文件，提供各种方法及前后置操作
│     ├── test_alarms.py				预警测试用例demo
│     └── test_login.py					预警测试用例demo
└── utils						测试工具存放目录
    ├── get_config.py					读取config配置文件的方法
    ├── get_dir_path.py					获取项目各个文件路径的类
    ├── get_yaml_data.py				读取yaml文件的方法
    ├── lock_reset.py					门禁出厂
    ├── temperature_terminal_reset.py			测温终端出厂
    └── time_utils.py					时间转换工具类
```

