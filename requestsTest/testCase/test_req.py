#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/15 18:05
# @Author : liujianxiao
# @Version：V 0.1
# @File : test_req.py
# @desc : 下单
import allure
import pytest

from requestsTest.testCase.test_Base import TestBase
from util import yamlUtil

@allure.feature("订单模块")
class TestOrder(TestBase):
    caseInformation = yamlUtil.readYaml(f"{TestBase.basedir}/file/case/order.yml")




    # 下单用例
    @allure.story("下单")
    @pytest.mark.parametrize("caseID,before,interfaceGroup,interfacekey,json,expectResult,setGlobal,after",
                             TestBase.getCaseInformation(caseInformation,"req"),
                             ids=TestBase.getAllCaseName(caseInformation,"req"))
    def test_req(self,caseID,before,interfaceGroup,interfacekey,json,expectResult,setGlobal,after):
        with allure.step("执行前置条件及请求接口"):
        # 请求接口
            requestResult = self.sendRequest(before,interfaceGroup,interfacekey,json)
        with allure.step("设置公共参数"):
        # 设置参数
            self.toSetGlobal(setGlobal, requestResult)
        with allure.step("结果断言"):
            try:
                # 参数断言
                self.assertJsonResult(expectResult.get("assertJson"), requestResult.json())
                # sql断言
                self.assertSqlResult(expectResult.get("assertSql"))
            except:
                raise RuntimeError("error")

            finally:
                with allure.step("执行后续操作"):
                    self.afterPrepare(after)


    # 取消用例
    @allure.story("取消订单")
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





