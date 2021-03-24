#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/14 15:18
# @Author : liujianxiao
# @Version：V 0.1
# @File : Base.py
# @desc : 基础类
import requests



class Base():
    # 初始化会话
    def __init__(self):
        self.request_session=requests.session()

    ## 发送请求
    def send(self,*args,**kwargs):
        return self.request_session.request(*args,**kwargs)

