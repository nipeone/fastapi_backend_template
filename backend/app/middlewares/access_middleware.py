#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   access_middleware.py
@Time    :   2024/04/13 19:49:30
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.app.common.log import log
from backend.app.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """记录请求日志中间件"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = timezone.now()
        response = await call_next(request)
        end_time = timezone.now()
        log.info(f'{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}')
        return response