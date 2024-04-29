#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   health_check.py
@Time    :   2024/04/13 20:13:19
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from math import ceil

from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute

from backend.app.common.exception import errors


def ensure_unique_route_names(app: FastAPI) -> None:
    """
    检查路由名称是否唯一

    :param app:
    :return:
    """
    temp_routes = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in temp_routes:
                raise ValueError(f'Non-unique route name: {route.name}')
            temp_routes.add(route.name)


async def http_limit_callback(request: Request, response: Response, expire: int):
    """
    请求限制时的默认回调函数

    :param request:
    :param response:
    :param expire: 剩余毫秒
    :return:
    """
    expires = ceil(expire / 1000)
    raise errors.HTTPError(code=429, msg='请求过于频繁，请稍后重试', headers={'Retry-After': str(expires)})
