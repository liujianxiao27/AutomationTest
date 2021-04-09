#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/14 15:23
# @Author : liujianxiao
# @Version：V 0.1
# @File : requestInterface.py
# @desc : 请求接口
import os

from requestsTest.requestsFramework.Base import Base
from util import yamlUtil


class RequestInterface(Base):
    basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    def __init__(self):
        self.enviromentInformation = yamlUtil.readYaml( f"{self.basedir}/file/interface/enviroment.yml")
        self.group = yamlUtil.readYaml(f"{self.basedir}/file/interface/group.yml")
        super().__init__()

    # 发送请求
    def sendRequests(self,interfaceGroupName,key,json:None):
        # 获取接口文件路径
        interfaceFilepath = self.getInterfaceFilepath(interfaceGroupName)
        if interfaceFilepath:
            # 获取接口信息
            interfaceInformation=yamlUtil.readYamlByKey(self.basedir + interfaceFilepath, key)
            if interfaceInformation:
                url = interfaceInformation.get("url")
                host=interfaceInformation.get("host")
                # 根据url和host拼接获取完整接口url
                fullUrl = self.jonitUrl(url,host)
                method=interfaceInformation.get("method")
                header=interfaceInformation.get("header")
                return self.send(method, fullUrl, headers=header, json=json)
            else:
                return None
        else:
            return None



    # 通过接口分组获取接口地址
    def getInterfaceFilepath(self,interfaceGroupName):
        interfaceFile = self.group.get("interface").get(interfaceGroupName) # 获取接口文件路径
        if interfaceFile:
            return interfaceFile
        else:
            return None


    # 拼接接口
    def jonitUrl(self,url,host):
            # 根据配置中的默认环境获取对应环境的host
            enviroment=self.enviromentInformation.get("defaultEnvironment").get("environment")
            realHost=self.enviromentInformation.get(enviroment).get(host)
            # 获取url
            realurl=realHost + url
            # 组装url结束，返回数据
            return realurl





