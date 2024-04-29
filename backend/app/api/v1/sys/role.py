#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   role.py
@Time    :   2024/04/21 14:47:40
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated, Optional, Union

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.schemas.role import CreateRoleParam, GetRoleListDetails, UpdateRoleMenuParam, UpdateRoleParam
from backend.app.services.service_menu import menu_service
from backend.app.services.service_role import role_service
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.common.security.permission import RequestPermission
from backend.app.common.security.rbac import DependsRBAC
from backend.app.utils.serializers import select_as_dict, select_list_serialize

router = APIRouter()

@router.get('/all', summary='获取所有角色', dependencies=[DependsJwtAuth])
async def get_all_roles() -> ResponseModel:
    roles = await role_service.all()
    data = await select_list_serialize(roles)
    return await response_base.success(data=data)

@router.get('/{pk}/all', summary='获取用户所有角色', dependencies=[DependsJwtAuth])
async def get_user_all_roles(pk: Annotated[int, Path(...)]) -> ResponseModel:
    roles = await role_service.get_user_roles(pk=pk)
    data = await select_list_serialize(roles)
    return await response_base.success(data=data)

@router.get('/{pk}/menus', summary='获取角色所有菜单', dependencies=[DependsJwtAuth])
async def get_role_all_menus(pk: Annotated[int, Path(...)]) -> ResponseModel:
    menu = await menu_service.get_role_menu_tree(pk=pk)
    return await response_base.success(data=menu)

@router.get('/{pk}', summary='获取角色详情', dependencies=[DependsJwtAuth])
async def get_role(pk: Annotated[int, Path(...)]) -> ResponseModel:
    role = await role_service.get(pk=pk)
    data = GetRoleListDetails(**await select_as_dict(role))
    return await response_base.success(data=data)

@router.get('', summary='（模糊条件）分页获取所有角色', dependencies=[DependsJwtAuth, DependsPagination])
async def get_pagination_roles(
    name: Annotated[Optional[str], Query()] = None,
    data_scope: Annotated[Optional[int], Query()] = None,
    status: Annotated[Optional[int], Query()] = None,
) -> ResponseModel:
    page_data = await role_service.get_pagination(name=name, data_scope=data_scope, status=status)
    return await response_base.success(data=page_data)

@router.post('', summary='创建角色', dependencies=[Depends(RequestPermission('sys:role:add')), DependsRBAC])
async def create_role(obj: CreateRoleParam) -> ResponseModel:
    await role_service.create(obj=obj)
    return await response_base.success()


@router.put('/{pk}', summary='更新角色', dependencies=[Depends(RequestPermission('sys:role:edit')), DependsRBAC])
async def update_role(pk: Annotated[int, Path(...)], obj: UpdateRoleParam) -> ResponseModel:
    count = await role_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()

@router.put('/{pk}/menu', summary='更新角色菜单', dependencies=[Depends(RequestPermission('sys:role:menu:edit')), DependsRBAC])
async def update_role_menus(
    request: Request, pk: Annotated[int, Path(...)], menu_ids: UpdateRoleMenuParam
) -> ResponseModel:
    count = await role_service.update_role_menu(request=request, pk=pk, menu_ids=menu_ids)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()

@router.delete('', summary='（批量）删除角色', dependencies=[Depends(RequestPermission('sys:role:del')), DependsRBAC])
async def delete_role(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await role_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()