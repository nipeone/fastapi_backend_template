#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   errors.py
@Time    :   2023/12/25 16:32:11
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
"""
全局业务异常类

业务代码执行异常时，可以使用 raise xxxError 触发内部错误，它尽可能实现带有后台任务的异常，但它不适用于**自定义响应状态码**
如果要求使用**自定义响应状态码**，则可以通过 return await response_base.fail(res=CustomResponseCode.xxx) 直接返回
"""  # noqa: E501
from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette.background import BackgroundTask

from backend.app.common.response.response_code import CustomErrorCode, StandardResponseCode


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None, background: Optional[BackgroundTask] = None):
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background

    def __str__(self) -> str:
        if self.data:
            return f"(code={self.code!r}, msg={self.msg!r}, detail={self.data!r})"
        else:
            return f"(code={self.code!r}, msg={self.msg!r})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.code!r}, msg={self.msg!r})"

class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=code, detail=msg, headers=headers)

    def __str__(self) -> str:
        return f"(code={self.status_code!r}, detail={self.detail!r})"

class CustomError(BaseExceptionMixin):
    def __init__(self, *, error: CustomErrorCode, data: Any = None, background: Optional[BackgroundTask] = None):
        self.code = error.code
        super().__init__(msg=error.msg, data=data, background=background)


class RequestError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_400

    def __init__(self, *, msg: str = 'Bad Request', data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(msg=msg, data=data, background=background)


class ForbiddenError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_403

    def __init__(self, *, msg: str = 'Forbidden', data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(msg=msg, data=data, background=background)


class NotFoundError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_404

    def __init__(self, *, msg: str = 'Not Found', data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(msg=msg, data=data, background=background)


class ServerError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_500

    def __init__(
        self, *, msg: str = 'Internal Server Error', data: Any = None, background: Optional[BackgroundTask] = None
    ):
        super().__init__(msg=msg, data=data, background=background)


class GatewayError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_502

    def __init__(self, *, msg: str = 'Bad Gateway', data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Permission Denied', data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(msg=msg, data=data, background=background)


class TokenError(HTTPError):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Not Authenticated', headers: Optional[Dict[str, Any]] = None):
        super().__init__(code=self.code, msg=msg, headers=headers or {'WWW-Authenticate': 'Bearer'})

# Task exeception
class TaskError(CustomError):
    error = CustomErrorCode.TASK_ERROR
    
    def __init__(self, *, data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(error=self.error, data=data, background=background)

class TaskNotFoundError(CustomError):
    error = CustomErrorCode.TASK_NOT_FOUND_ERROR
    
    def __init__(self, *, data: Any = None, background: Optional[BackgroundTask] = None):
        super().__init__(error=self.error, data=data, background=background)
