#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dept.py
@Time    :   2024/04/21 16:31:26
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, Query

from backend.app.schemas.dept import CreateDeptParam, GetDeptListDetails, UpdateDeptParam
from backend.app.services.service_dept import dept_service
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.common.security.permission import RequestPermission
from backend.app.common.security.rbac import DependsRBAC
from backend.app.utils.serializers import select_as_dict

router = APIRouter()

@router.get('/{pk}', summary='获取部门详情', dependencies=[DependsJwtAuth])
async def get_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    dept = await dept_service.get(pk=pk)
    data = GetDeptListDetails(**await select_as_dict(dept))
    return await response_base.success(data=data)


@router.get('', summary='获取所有部门展示树', dependencies=[DependsJwtAuth])
async def get_all_depts_tree(
    name: Annotated[Optional[str], Query()] = None,
    leader: Annotated[Optional[str], Query()] = None,
    phone: Annotated[Optional[str], Query()] = None,
    status: Annotated[Optional[int], Query()] = None,
) -> ResponseModel:
    dept = await dept_service.get_dept_tree(name=name, leader=leader, phone=phone, status=status)
    return await response_base.success(data=dept)


@router.post('', summary='创建部门', dependencies=[Depends(RequestPermission('sys:dept:add')), DependsRBAC])
async def create_dept(obj: CreateDeptParam) -> ResponseModel:
    await dept_service.create(obj=obj)
    return await response_base.success()


@router.put('/{pk}', summary='更新部门', dependencies=[Depends(RequestPermission('sys:dept:edit')), DependsRBAC])
async def update_dept(pk: Annotated[int, Path(...)], obj: UpdateDeptParam) -> ResponseModel:
    count = await dept_service.update(dept_id=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('/{pk}', summary='删除部门', dependencies=[Depends(RequestPermission('sys:dept:del')), DependsRBAC])
async def delete_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await dept_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()