#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/15 18:05
# @Author : liujianxiao
# @Version：V 0.1
# @File : test_req.py
# @desc : 下单
import pytest

from requestsTest.testCase.test_Base import TestBase
from util import yamlUtil


class TestOrder(TestBase):
    caseInformation = yamlUtil.readYaml("../file/case/order.yml")




    # 下单用例
    # @pytest.mark.skip()
    @pytest.mark.parametrize("caseID,before,interfaceGroup,interfacekey,json,expectResult,setGlobal,after",
                             TestBase.getCaseInformation(caseInformation,"req"),
                             ids=TestBase.getAllCaseName(caseInformation,"req"))
    def test_req(self,caseID,before,interfaceGroup,interfacekey,json,expectResult,setGlobal,after):
        # 请求接口
        requestResult = self.sendRequest(before,interfaceGroup,interfacekey,json)
        # 设置参数
        self.toSetGlobal(setGlobal, requestResult)
        try:
            # 参数断言
            self.assertJsonResult(expectResult.get("assertJson"), requestResult.json())
            # sql断言
            self.assertSqlResult(expectResult.get("assertSql"))
        except:
            raise RuntimeError("error")

        finally:
            self.afterPrepare(after)


    # 取消用例
    @pytest.mark.parametrize("caseID,before,interfaceGroup,interfacekey,json,expectResult,setGlobal,after",
                             TestBase.getCaseInformation(caseInformation, "cancel"),
                             ids=TestBase.getAllCaseName(caseInformation, "cancel"))
    def test_cancel(self,caseID,before,interfaceGroup,interfacekey,json,expectResult,setGlobal,after):
        # 请求接口
        requestResult=self.sendRequest(before, interfaceGroup, interfacekey, json)
        # 设置参数
        self.toSetGlobal(setGlobal, requestResult)
        try:
            # 参数断言
            self.assertJsonResult(expectResult.get("assertJson"), requestResult.json())
            # sql断言
            self.assertSqlResult(expectResult.get("assertSql"))

        except:
            raise RuntimeError("error")

        finally:
            self.afterPrepare(after)





