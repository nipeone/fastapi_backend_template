#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   jwt_auth_middleware.py
@Time    :   2024/04/13 19:04:36
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional, Any, Dict
from fastapi import Request, Response
from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials
from starlette.requests import HTTPConnection

from backend.app.core.conf import settings
from backend.app.common.security import jwt
from backend.app.common.exception.errors import TokenError
from backend.app.common.log import log
from backend.app.utils.serializers import MsgSpecJSONResponse

class _AuthenticationError(AuthenticationError):
    """重写内部认证错误类"""

    def __init__(self, *, code: int = None, msg: str = None, headers: Optional[Dict[str, Any]] = None):
        self.code = code
        self.msg = msg
        self.headers = headers

class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: _AuthenticationError) -> Response:
        """覆盖内部认证错误处理"""
        return MsgSpecJSONResponse(content={'code': exc.code, 'msg': exc.msg, 'data': None}, status_code=exc.code)

    async def authenticate(self, request: Request):
        auth = request.headers.get('Authorization')
        if not auth:
            return

        if request.url.path in settings.TOKEN_EXCLUDE:
            return

        scheme, token = auth.split()
        if scheme.lower() != 'bearer':
            return

        try:
            user = await jwt.jwt_authentication(token)
        except TokenError as exc:
            raise _AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception as e:
            log.exception(e)
            raise _AuthenticationError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        # 请注意，此返回使用非标准模式，所以在认证通过时，将丢失某些标准特性
        # 标准返回模式请查看：https://www.starlette.io/authentication/
        return AuthCredentials(['authenticated']), user