#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/17 13:36
# @Author : liujianxiao
# @Version：V 0.1
# @File : conftest.py.py
# @desc :
from typing import List



# @pytest.mark.parametrize装饰器ids使用中文
def pytest_collection_modifyitems(session: "Session", config: "Config", items: List["Item"]) -> None:
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')