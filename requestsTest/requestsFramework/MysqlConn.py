#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/17 15:07
# @Author : liujianxiao
# @Version：V 0.1
# @File : MysqlConn.py
# @desc : 连接mysql
import os

import pymysql

from util import yamlUtil


class MySqlConn():
    def __init__(self):
        # 初始化连接数据库
        self.conn = self.conn()
        self.cursor = self.conn.cursor()

    # 连接数据库
    def conn(self):
        basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        getEnviroment = yamlUtil.readYaml(f"{basedir}/file/interface/enviroment.yml")
        enviromrnt = getEnviroment.get("defaultEnvironment").get("environment")
        mysqlInformation = getEnviroment.get(enviromrnt).get("sql")
        if mysqlInformation :
            host=mysqlInformation.get("host")
            port=mysqlInformation.get("port")
            user=mysqlInformation.get("user")
            password=mysqlInformation.get("password")
            charset=mysqlInformation.get("charset")
            connection = pymysql.connect(host=host,port=port,user=user,password=password,charset=charset)
            return connection
        else:
            return None

    # 提交修改表的sql（增删改）
    def performSql(self,sql):
        result = self.cursor.execute(sql)
        self.conn.commit()

    # 提交查询sql
    def performSelectSql(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        titletuple = self.cursor.description
        titlelist = []
        for title in titletuple:
            titlelist.append(title[0])
        resultdir = dict(zip(titlelist,result[0]))
        return resultdir

