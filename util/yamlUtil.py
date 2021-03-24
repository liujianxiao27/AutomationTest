#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/14 15:15
# @Author : liujianxiao
# @Version：V 0.1
# @File : yamlUtil.py
# @desc : yaml工具类

import yaml

# 读取yaml文件
def readYaml(filepath):
    with open(filepath,encoding="utf8") as file:
        result = yaml.safe_load(file)
        return result

# 根据key读取yaml文件内容
def readYamlByKey(filepath,key):
    allResult = readYaml(filepath)
    return allResult.get(key)
