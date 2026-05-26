# SensoroApiAutoTest

基于 Python + pytest + requests + Allure 的 API 自动化测试框架，遵循 PO 设计模式。

## 联系方式

- CSDN博客：https://blog.csdn.net/weixin_65784341?spm=1011.2415.3001.5343
- 对本框架有任何疑问均可加我微信拉你入自动化交流群(记得备注添加原因)：wj1641540482

![微信二维码](files/images/微信二维码.png)

## 已支持功能

- 测试数据隔离，支持数据驱动（YAML 参数化）
- 环境一键切换（命令行 `-env` 参数），多环境互不干扰
- 多接口数据依赖：如 A 接口依赖 B、C 接口的响应数据作为参数
- 数据库集成：查询结果可直接用于断言操作
- 消息通知：支持邮件、企业微信群通知
- 自定义扩展方法：用例中可直接调用随机数据、时间工具等
- 统计接口运行时长，每条 case 耗时一目了然
- 多种报告：pytest-html 及 Allure，可动态切换
- 日志模块：可开关，按需打印接口请求/响应详情

## 规划中

- 自动生成用例代码：测试人员在 yaml 中填写用例，程序直接生成用例代码
- 接口录制：录制包含 url 的接口，自动生成用例数据
- 动态多断言：同时校验响应数据 + SQL 等多场景断言
- swagger 接口文档转 yaml 用例
- 集成 UI 自动化、关键字驱动

## 环境准备

**技术栈**：python 3.10+ | pytest | requests | allure | pytest-html | pycharm | jenkins | gitlab

## 安装依赖

获取源码后，在终端运行：

```bash
pip3 install -r requirements.txt
```

> Windows 下如报 `UnicodeDecodeError: 'gbk' codec can't decode byte`，先执行 `chcp 65001` 再安装。

也可以直接用 pycharm 自带的提示功能安装依赖包（推荐）。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 查看目标环境配置（按需修改 base_url）
cat config/environments.yaml

# 3. 运行测试（默认 TEST 环境，使用 JSONPlaceholder 示例 API）
python run.py -env TEST

# 指定环境并开启通知
python run.py -env DEV --send-wechat True --send-email True
```

## 项目结构

```
├── README.md
├── apis                    业务接口层（PO 模式）
│   └── user_api.py         Demo：用户模块接口
├── config                  配置文件
│   ├── environments.yaml   多环境配置（URL / headers / 数据库）
│   └── settings.yaml       运行参数、通知开关
├── conftest.py             pytest 全局配置（报告美化、控制台摘要）
├── core                    公共基础模块
│   ├── config_manager.py   统一配置管理器
│   ├── exceptions.py       自定义异常
│   ├── http_client.py      HTTP 客户端（对 requests 二次封装）
│   ├── logger.py           日志记录器
│   ├── models.py           数据模型（HTTP 方法枚举等）
│   └── paths.py            目录路径定义（基于 pathlib）
├── data                    测试数据（YAML）
│   └── user.yaml           Demo：用户测试数据
├── files                   静态资源
│   └── images/             文档图片
├── output                  构建产物
│   ├── allure_report/      Allure HTML 报告
│   ├── allure_result/      Allure 原始数据
│   ├── logs/               运行日志
│   ├── pytest_report/      pytest-html 报告
│   └── pytest_result/      pytest-json 报告
├── pytest.ini
├── requirements.txt
├── run.py                  测试执行入口
├── testcase                测试用例
│   ├── conftest.py         fixture 定义（http_client、user_api 等）
│   └── test_user.py        Demo：用户模块测试用例
└── utils                   工具类
    ├── allure_util.py      Allure 报告美化
    ├── cache_util.py       跨用例数据缓存
    ├── command_parser.py   命令行参数解析
    ├── connect_db.py       数据库连接（MySQL / PostgreSQL）
    ├── data_util.py        数据模板处理
    ├── excel_util.py       Excel 文件操作
    ├── faker_util.py       随机数据生成
    ├── file_util.py        文件处理
    ├── get_local_ip.py     获取本机 IP
    ├── jenkins_util.py     Jenkins 集成
    ├── mail_sender.py      邮件发送
    ├── MIME_type_classifier.py  MIME 类型识别
    ├── report_data_handle.py    测试结果统计
    ├── robot_sender.py     企业微信通知
    ├── time_util.py        时间工具
    └── yaml_util.py        YAML 文件操作
```

## 框架设计

### 设计原则

- **封装基类**：通用方法（发送请求、增删改查）统一封装在 `HttpClient` 中
- **高内聚低耦合**：每个模块独立完成自身功能，模块间接口尽量简单
- **脚本分离**：业务代码、测试数据、配置相互剥离，遵循 PO 设计模式

### 调用链路

```
run.py
   |
   +-- pytest 调用
   |      |
   |      v
   |   testcase/test_xxx.py  (pytest 测试)
   |      |                           +-- data/*.yaml (测试数据)
   |      |                           +-- testcase/conftest.py (fixtures)
   |      v
   |   apis/xxx_api.py  (业务 API 封装)
   |      |
   |      v
   |   core/http_client.py  (HTTP 请求封装)
   |      |
   |      v
   |   config/environments.yaml  (环境: URL, headers, 数据库)
   |
   +-- 后处理
      |
      +-- Allure 报告生成与定制
      +-- 通知（企业微信 / 邮件）
```

## 配置说明

### 环境配置（`config/environments.yaml`）

```yaml
TEST:
  base_url: https://jsonplaceholder.typicode.com
  default_headers:
    Content-Type: application/json;charset=UTF-8

DEV:
  base_url: https://jsonplaceholder.typicode.com
  default_headers:
    Content-Type: application/json;charset=UTF-8

PROD:
  base_url: https://jsonplaceholder.typicode.com
  default_headers:
    Content-Type: application/json;charset=UTF-8
```

> 支持的环境名在 `environments.yaml` 的顶级 key 中定义，通过 `python run.py -env <NAME>` 切换。

### 运行配置（`config/settings.yaml`）

```yaml
project:
  name: API Automation Test Demo
  default_env: TEST          # 默认运行环境

runtime:
  max_fail_count: 100        # 最大失败数后停止
  rerun_count: 1             # 失败重跑次数
  rerun_delay_seconds: 3     # 重跑间隔（秒）
  log_level: INFO            # 日志等级
  console_log: True          # 是否开启控制台日志

notifications:
  email:
    enabled: False
    ...
  wechat:
    enabled: False
    webhook_urls: ['https://qyapi.weixin.qq.com/...']
```

## 编写用例

### 1. 定义接口（`apis/`）

使用 Pydantic 校验请求参数，通过 `HttpClient` 依赖注入发起请求：

```python
# apis/user_api.py
from pydantic import BaseModel, ConfigDict, Field
from core.http_client import HttpClient

class CreatePostParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., description="帖子标题")
    body: str = Field(..., description="帖子内容")
    userId: int = Field(..., description="用户ID")

class UserApi:
    def __init__(self, client: HttpClient):
        self._client = client

    def get_users(self, headers: dict = None) -> Response:
        return self._client.get('/users', headers=headers)

    def get_user(self, user_id: int, headers: dict = None) -> Response:
        return self._client.get(f'/users/{user_id}', headers=headers)

    def create_post(self, title: str, body: str, user_id: int, headers: dict = None) -> Response:
        params = CreatePostParams(title=title, body=body, userId=user_id)
        return self._client.post('/posts', json_data=params.model_dump(), headers=headers)
```

### 2. 准备测试数据（`data/`）

```yaml
# data/user.yaml
- case_title: "获取单个用户"
  user_id: 1
  expected_name: "Leanne Graham"

- case_title: "获取不存在的用户"
  user_id: 999
  expected_status: 404
```

### 3. 编写测试用例（`testcase/`）

通过 fixture 注入 `HttpClient`，数据驱动 + allure 报告注解：

```python
# testcase/test_user.py
from core.paths import DATAS_DIR
from utils.yaml_util import YamlUtil

_params = [(item['case_title'], item.get('user_id'), item.get('expected_name'),
            item.get('expected_status')) for item in YamlUtil.read_yaml(DATAS_DIR / 'user.yaml')]

@allure.feature("用户模块")
class TestUser:

    @allure.title('{case_title}')
    @pytest.mark.parametrize('case_title, user_id, expected_name, expected_status', _params)
    def test_get_user(self, case_title, user_id, expected_name, expected_status,
                      user_api: UserApi, http_client: HttpClient):
        response = user_api.get_user(user_id)
        if expected_status:
            assert http_client.get_status_code(response) == expected_status
        else:
            assert http_client.get_json(response)['name'] == expected_name
```

### 4. 运行

```bash
python run.py                        # 默认 TEST 环境
python run.py -env DEV               # 指定 DEV 环境
python run.py -env TEST --send-wechat True --send-email True  # 开启通知
```

## 报告展示

- 总览：

![总览.png](files/images/报告图片/总览.png)

- 单个用例运行详情：

![单个用例详情.png](files/images/报告图片/单个用例详情.png)

- 图表：

![图表.png](files/images/报告图片/图表.png)

- 时间刻度：

![时间刻度.png](files/images/报告图片/时间刻度.png)
