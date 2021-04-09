#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/19 16:46
# @Author : liujianxiao
# @Version：V 0.1
# @File : RedisConn.py
# @desc : redis操作
import os

import redis

from util import yamlUtil


class RedisConn():
    def __init__(self):
        self.reidsConn = self.conn() # 连接redis

    def conn(self):
        basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        getEnviroment=yamlUtil.readYaml(f"{basedir}/file/interface/enviroment.yml")
        enviromrnt=getEnviroment.get("defaultEnvironment").get("environment")
        redisInformation = getEnviroment.get(enviromrnt).get("redis")
        if redisInformation:
            host=redisInformation.get("host")
            port=redisInformation.get("port")
            db=redisInformation.get("db")
            r=redis.StrictRedis(host=host, port=port, db=db)
            return r
        else:
            return None

    # 获取
    def get(self,key):
        return self.reidsConn.get(key)

    # 修改
    def get(self,key,value):
        self.reidsConn.set(key,value)

    # 删除
    def delete(self,key):
        self.reidsConn.delete(key)

