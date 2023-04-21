# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/4/21 10:36
# @Author : wangjie
# @File : connect_DB.py
# @project : SensoroApi
import psycopg2
import psycopg2.pool
import pymysql
from dbutils.pooled_db import PooledDB


class Postgresql:
    """连接Postgresql数据库"""

    def __init__(self, db_config, minconn=1, maxconn=10):
        self.db_config = db_config
        self.minconn = minconn
        self.maxconn = maxconn
        self.pool = None

    def connect(self):
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(
                self.minconn, self.maxconn, **self.db_config)
            print("Database connected successfully")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query):
        conn = None
        try:
            with self.pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    conn.commit()
                    print("Query executed successfully")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
        finally:
            if conn:
                self.pool.putconn(conn)

    def execute_query_with_result(self, query):
        conn = None
        try:
            with self.pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    return results
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if conn:
                self.pool.putconn(conn)

    def disconnect(self):
        if self.pool:
            self.pool.closeall()
            print("Database disconnected")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


class MySQL:
    """连接MySQL数据库"""

    def __init__(self, db_config, minconn=1, maxconn=10):
        self.db_config = db_config
        self.minconn = minconn
        self.maxconn = maxconn
        self.pool = None

    def connect(self):
        try:
            self.pool = PooledDB(
                creator=pymysql,  # 使用pymysql库
                maxconnections=self.maxconn,
                mincached=self.minconn,
                maxcached=self.maxconn,
                **self.db_config
            )
            print("Database connected successfully")
        except pymysql.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query):
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    conn.commit()
                    print("Query executed successfully")
        except pymysql.Error as e:
            print(f"Error executing query: {e}")

    def execute_query_with_result(self, query):
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    return results
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None

    def disconnect(self):
        if self.pool:
            self.pool.close()
            print("Database disconnected")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


if __name__ == '__main__':
    # db_config = {
    #     "host": "pg-cluster-lins.postgres",
    #     "port": 5432,
    #     "database": "postgres",
    #     "user": "lins",
    #     "password": "lins"
    # }
    #
    # with Postgresql(db_config) as db:
    #     db.execute_query("SELECT * FROM mytable")

    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'autotest',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }

    with MySQL(db_config) as db:
        query = "SELECT * FROM student WHERE name = '张三'"
        result = db.execute_query_with_result(query)
        print(result)
