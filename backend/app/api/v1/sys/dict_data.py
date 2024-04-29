#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dict_data.py
@Time    :   2024/04/21 16:58:49
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, Query

from backend.app.schemas.dict_data import CreateDictDataParam, GetDictDataListDetails, UpdateDictDataParam
from backend.app.services.service_dict_data import dict_data_service
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.common.security.permission import RequestPermission
from backend.app.common.security.rbac import DependsRBAC
from backend.app.utils.serializers import select_as_dict

router = APIRouter()

@router.get('/{pk}', summary='获取字典详情', dependencies=[DependsJwtAuth])
async def get_dict_data(pk: Annotated[int, Path(...)]) -> ResponseModel:
    dict_data = await dict_data_service.get(pk=pk)
    data = GetDictDataListDetails(**await select_as_dict(dict_data))
    return await response_base.success(data=data)


@router.get('', summary='（模糊条件）分页获取所有字典', dependencies=[DependsJwtAuth, DependsPagination])
async def get_pagination_dict_datas(
    label: Annotated[Optional[str], Query()] = None,
    value: Annotated[Optional[str], Query()] = None,
    status: Annotated[Optional[int], Query()] = None,
) -> ResponseModel:
    page_data = await dict_data_service.get_pagination(label=label, value=value, status=status)
    return await response_base.success(data=page_data)


@router.post('', summary='创建字典', dependencies=[Depends(RequestPermission('sys:dict:data:add')), DependsRBAC])
async def create_dict_data(obj: CreateDictDataParam) -> ResponseModel:
    await dict_data_service.create(obj=obj)
    return await response_base.success()


@router.put('/{pk}', summary='更新字典', dependencies=[Depends(RequestPermission('sys:dict:data:edit')), DependsRBAC])
async def update_dict_data(pk: Annotated[int, Path(...)], obj: UpdateDictDataParam) -> ResponseModel:
    count = await dict_data_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('', summary='（批量）删除字典', dependencies=[Depends(RequestPermission('sys:dict:data:del')), DependsRBAC])
async def delete_dict_data(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await dict_data_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()