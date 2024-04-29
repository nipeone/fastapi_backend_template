#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   response_schema.py
@Time    :   2024/04/13 18:09:51
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Set, Dict, Union, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from backend.app.common.response.response_code import CustomResponse, CustomResponseCode
from backend.app.core.conf import settings

class ResponseModel(BaseModel):
    """
    统一返回模型

    E.g. ::

        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            res = CustomResponseCode.HTTP_200
            return ResponseModel(code=res.code, msg=res.msg, data={'test': 'test'})
    """

    # TODO: json_encoders 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Optional[Any] = None

class ResponseBase:
    """
    统一返回方法

    .. tip::

        此类中的方法将返回 ResponseModel 模型，作为一种编码风格而存在；

    E.g. ::

        @router.get('/test')
        def test() -> ResponseModel:
            return await response_base.success(data={'test': 'test'})
    """

    async def __response(self, *, res: Union[CustomResponseCode, CustomResponse] = None, data: Optional[Any] = None) -> ResponseModel:
        """
        请求成功返回通用方法

        :param res: 返回信息
        :param data: 返回数据
        :return:
        """
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    async def success(
        self,
        *,
        res: Union[CustomResponseCode, CustomResponse] = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> ResponseModel:
        return await self.__response(res=res, data=data)

    async def fail(
        self,
        *,
        res: Union[CustomResponseCode, CustomResponse] = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel:
        return await self.__response(res=res, data=data)


response_base = ResponseBase()