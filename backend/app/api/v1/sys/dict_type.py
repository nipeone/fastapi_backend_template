#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dict_type.py
@Time    :   2024/04/21 16:56:24
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, Query

from backend.app.schemas.dict_type import CreateDictTypeParam, GetDictTypeListDetails, UpdateDictTypeParam
from backend.app.services.service_dict_type import dict_type_service
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.common.security.permission import RequestPermission
from backend.app.common.security.rbac import DependsRBAC

router = APIRouter()

@router.get('', summary='（模糊条件）分页获取所有字典类型', dependencies=[DependsJwtAuth, DependsPagination])
async def get_pagination_dict_types(
    name: Annotated[Optional[str], Query()] = None,
    code: Annotated[Optional[str], Query()] = None,
    status: Annotated[Optional[int], Query()] = None,
) -> ResponseModel:
    page_data = await dict_type_service.get_pagination(name=name, code=code, status=status)
    return await response_base.success(data=page_data)


@router.post('', summary='创建字典类型', dependencies=[Depends(RequestPermission('sys:dict:type:add')), DependsRBAC])
async def create_dict_type(obj: CreateDictTypeParam) -> ResponseModel:
    await dict_type_service.create(obj=obj)
    return await response_base.success()


@router.put('/{pk}', summary='更新字典类型', dependencies=[Depends(RequestPermission('sys:dict:type:edit')), DependsRBAC])
async def update_dict_type(pk: Annotated[int, Path(...)], obj: UpdateDictTypeParam) -> ResponseModel:
    count = await dict_type_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('', summary='（批量）删除字典类型', dependencies=[Depends(RequestPermission('sys:dict:type:del')), DependsRBAC])
async def delete_dict_type(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await dict_type_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()