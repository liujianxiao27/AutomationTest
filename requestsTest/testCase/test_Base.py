#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/15 17:45
# @Author : liujianxiao
# @Version：V 0.1
# @File : test_Base.py
# @desc :
import json
import re

import pytest
from jsonpath import jsonpath

from requestsTest.requestsFramework.MysqlConn import MySqlConn
from requestsTest.requestsFramework.RedisConn import RedisConn
from requestsTest.requestsFramework.requestInterface import RequestInterface
from util import yamlUtil


class TestBase():
    requests = RequestInterface()   # 接口请求
    sqlConn = MySqlConn() # mysql操作
    redisConn = RedisConn() # redis操作

    globalParameters = dict() # 全局变量


    # 接口前期准备及接口调用返回结果
    def sendRequest(self,beforeInformation,interfaceGroup,interfacekey,json):
        # 接口调用进行前置准备
        self.beforePrepare(beforeInformation)
        #处理json
        self.jsonAssembly(json)
        print("json:",json)
        # 接口调用
        requestResult = self.requests.sendRequests(interfaceGroup,interfacekey,json)
        return requestResult





    # 将返回参数中字段设置为公共参数
    def toSetGlobal(self,setGlobalInformation,responseJson:json):
        if setGlobalInformation:
            setFlag = setGlobalInformation.get("isSet")
            if setFlag == 1:
                globalKeydirct = setGlobalInformation.get("setKey")
                for key in globalKeydirct:
                    value = jsonpath(responseJson.json(),f'$.{globalKeydirct.get(key)}')
                    if value:
                        self.globalParameters[key]=value[0]
                    print("globalKeydirct.get(key):",globalKeydirct.get(key))
                    print("responseJson:",responseJson.json())
                    print("globalParameters:", self.globalParameters)
            else:
                pass
        else:
            pass

    # json数据组装
    def jsonAssembly(self,jsonstr:json):
        for key in jsonstr:
            value = jsonstr.get(key) # 循环key值将value取出
            if value is json:
                # 若key对应的值为json格式则递归循环
                self.jsonAssembly(value)
            elif value is list:
                # 若可以对应的值为list格式则循环判断下一级
                for listValue in value:
                    # list嵌套json递归
                    self.jsonAssembly(listValue)
            elif value == None or value == "":
                # 若key对应的值为空则不处理
                pass
            else:
                # 其余情况暂定为 正常键值队的值
                if value[0] == "{":
                    # 若第一个字符及最后一个字符是{}说明要替换值
                    globaKey = value[1:-1]
                    print(globaKey)
                    jsonstr[key] = self.globalParameters.get(globaKey)
                else:
                    pass



    # 前置准备
    def beforePrepare(self, beforeInformation):
        if beforeInformation :
            caseList = beforeInformation.get("caseId")
            sqlList = beforeInformation.get("sql")
            redisList = beforeInformation.get("redis")
            if caseList :
                # 处理调用前置用例接口
                for caseinfo in caseList:
                    filepath = caseinfo.get("filepath")
                    key = caseinfo.get("key")
                    caseID = caseinfo.get("caseID")
                    self.callCase(filepath,key,caseID)
            if sqlList :
                # 处理调用前置sql 此处sql只做增删改的操作
                for sql in sqlList:
                    try:
                        self.sqlConn.performSql(sql)
                    except Exception:
                        print("运行时异常")
            if redisList:
                # 处理调用前置redis 此处sql只做删除操作
                for reidsKey in redisList:
                    self.redisConn.delete(reidsKey)
        else:
            pass


    # 后置准备
    def afterPrepare(self,afterInformation):
        if afterInformation:
            caseList=afterInformation.get("caseId")
            sqlList=afterInformation.get("sql")
            redisList=afterInformation.get("redis")
            if caseList:
                # 处理调用用例接口
                for caseinfo in caseList:
                    filepath=caseinfo.get("filepath")
                    key=caseinfo.get("key")
                    caseID=caseinfo.get("caseID")
                    self.callCase(filepath, key, caseID)
            if sqlList:
                # 处理调用sql 此处sql只做增删改的操作
                for sql in sqlList:
                    try:
                        self.sqlConn.performSql(sql)
                    except Exception:
                        print("运行时异常")
            if redisList:
                # 处理调用redis 此处sql只做删除操作
                for reidsKey in redisList:
                    self.redisConn.delete(reidsKey)
        else:
            pass


    # 调用测试用例 处理前置用例或后置用例
    def callCase(self,filepath,key,caseId):
        caseInformation = yamlUtil.readYaml(filepath)
        Casees = caseInformation.get(key)
        for case in Casees:
            if case.get("caseID") == caseId:
                before = case.get("before")
                interfaceGroup = case.get("interfaceGroup")
                interfacekey = case.get("interfacekey")
                json = case.get("json")
                setGlobal = case.get("setGlobal")
                requestResult = self.sendRequest(before,interfaceGroup,interfacekey,json)
                self.toSetGlobal(setGlobal,requestResult)
            else:
                pass






    # caseInformation case文件信息
    # caseKey 文件信息中主键
    # 获取case下所有caseName，作为用例title使用
    @staticmethod
    def getAllCaseName(caseInformation, caseKey):
        caseNameList=[]
        for case in caseInformation.get(caseKey):
            caseNameList.append(case.get("caseName"))
        return caseNameList

    # 读取用例参数
    @staticmethod
    def getCaseInformation(caseInformation,caseKey):
        casesInformationList = [] # 测试用例信息
        for case in caseInformation.get(caseKey):
            caselist = [] # 单个用例信息，存在元组
            for key in case:
                if key == "caseName":
                    pass
                else:
                    caselist.append(case.get(key))
            casesInformationList.append(caselist)
        return casesInformationList


    # 断言Json结果是否相同
    def assertJsonResult(self,expect:dict,actual):
        for key in expect:
            expectValue = expect.get(key)
            actuallist = jsonpath(actual,f'$.{key}')
            if actuallist is None:
                actualValue = None
            else:
                actualValue = actuallist[0]

            pytest.assume(expectValue == actualValue,f"actualValue:{actualValue},expectValue:{expectValue}")

    # sql断言与预期值是否相同
    def assertSqlResult(self,sqlinfolist):
        if sqlinfolist:
            for sqlinfo in sqlinfolist:
                sql=sqlinfo.get("sql")
                assertdirct=sqlinfo.get("result")
                if sql is not None and assertdirct is not None:
                    # 使用正则将所有大括号及内容匹配为数组
                    sqlKey=re.findall(r'({.*?})', sql)
                    # 使用for循环将sql语句拼接完整
                    for key in sqlKey:
                        value=self.globalParameters.get(key[1:-1])
                        sql=sql.replace(key, value)
                    # 获取查询结果
                    sqlResult=self.sqlConn.performSelectSql(sql)
                    # for循环取出key值比对期望值与实际值
                    for key in assertdirct:
                        expectvalue=assertdirct.get(key)
                        actualvalue=sqlResult.get(key)
                        pytest.assume(str(expectvalue) == str(actualvalue), f"比对的数据库字段{key},期望值：{expectvalue},实际值：{actualvalue}")












