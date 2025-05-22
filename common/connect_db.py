#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/4/21 10:36
# @Author : wangjie
# @File : connect_db.py
# @project : SensoroApiAutoTest
import psycopg2
import psycopg2.pool
import pymysql
from dbutils.pooled_db import PooledDB

from common.base_log import logger
from configs.env_config import EnvConfig


class Postgresql:
    """连接Postgresql数据库"""

    def __init__(self, db_config, minconn=1, maxconn=10):
        self.db_config = db_config  # 数据库配置信息
        self.minconn = minconn  # 连接池最小连接数
        self.maxconn = maxconn  # 连接池最大连接数
        self.pool = None  # 连接池对象

    def connect(self):
        try:
            # 创建连接池
            self.pool = psycopg2.pool.SimpleConnectionPool(
                self.minconn, self.maxconn, **self.db_config)
            logger.info("数据库连接成功")
        except psycopg2.Error as e:
            logger.error(f"连接数据库错误: {e}")
            raise

    def execute_sql(self, sql):
        """
        执行新增、修改、删除sql
        :param sql: sql语句
        :return:
        """
        conn = None
        try:
            # 从连接池中获取1个连接
            with self.pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    conn.commit()
                    logger.info("执行sql成功")
        except psycopg2.Error as e:
            logger.error(f"执行sql错误: {e}")
        finally:
            if conn:
                self.pool.putconn(conn)  # 将连接归还到连接池

    def execute_query_with_result(self, sql):
        """
        执行查询sql并获取返回结果
        :param sql: 查询sql
        :return:
        """
        conn = None
        try:
            # 从连接池中获取1个连接
            with self.pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    results = cur.fetchall()
                    logger.info(f"执行sql成功,查询结果为：{results}")
                    return results
        except psycopg2.Error as e:
            logger.error(f"执行sql错误: {e}")
        finally:
            if conn:
                self.pool.putconn(conn)  # 将连接归还到连接池

    def disconnect(self):
        """断开数据库连接"""
        if self.pool:
            self.pool.closeall()
            logger.info("数据库断开连接")

    def __enter__(self):
        """进入上下文环境时执行的操作"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文环境时执行的操作"""
        self.disconnect()


class MySQL:
    """连接MySQL数据库"""

    def __init__(self, db_config, minconn=1, maxconn=10):
        self.db_config = db_config  # 数据库配置信息
        self.minconn = minconn  # 连接池最小连接数
        self.maxconn = maxconn  # 连接池最大连接数
        self.pool = None  # 连接池对象

    def connect(self):
        """链接数据库"""
        try:
            # 创建连接池
            self.pool = PooledDB(
                creator=pymysql,  # 使用pymysql库
                maxconnections=self.maxconn,
                mincached=self.minconn,
                maxcached=self.maxconn,
                cursorclass=pymysql.cursors.DictCursor,  # 使查询的结构返回为字典格式，默认为元组格式
                **self.db_config
            )
            logger.info("数据库连接成功")
        except pymysql.Error as e:
            logger.error(f"连接数据库错误: {e}")
            raise

    def execute_sql(self, sql):
        """
        执行新增、修改、删除sql
        :param sql: sql语句
        :return:
        """
        try:
            # 从连接池中获取1个连接
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    conn.commit()
                    logger.info("执行sql成功")
        except pymysql.Error as e:
            logger.error(f"执行sql错误: {e}")

    def execute_query_with_result(self, sql):
        """
        执行查询sql并获取返回结果
        :param sql: 查询sql
        :return:
        """
        try:
            # 从连接池中获取1个连接
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    results = cur.fetchall()
                    logger.info(f"执行sql成功,查询结果为：{results}")
                    return results
        except psycopg2.Error as e:
            logger.error(f"执行sql错误: {e}")

    def disconnect(self):
        """断开数据库连接"""
        if self.pool:
            self.pool.close()
            logger.info("数据库断开连接")

    def __enter__(self):
        """进入上下文环境时执行的操作"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文环境时执行的操作"""
        self.disconnect()


if __name__ == '__main__':
    # db_config = {
    #     "host": "xxxxxxxx",
    #     "port": xxxx,
    #     "database": "postgres",
    #     "user": "xxxx",
    #     "password": "xxxx"
    # }
    #
    # with Postgresql(db_config) as db:
    #     db.execute_query("SELECT * FROM mytable")

    db_config = EnvConfig.DB_CONFIG()
    with MySQL(db_config) as db:
        query = "SELECT * FROM student WHERE name = '张三'"
        result = db.execute_query_with_result(query)
        print(result)
