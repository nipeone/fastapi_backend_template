#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   openapi.py
@Time    :   2024/04/13 20:14:39
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from fastapi import FastAPI
from fastapi.routing import APIRoute


def simplify_operation_ids(app: FastAPI) -> None:
    """
    简化操作 ID，以便生成的客户端具有更简单的 api 函数名称

    :param app:
    :return:
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
