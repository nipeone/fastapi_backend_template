#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   menu.py
@Time    :   2024/04/21 14:52:52
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.schemas.menu import CreateMenuParam, GetMenuListDetails, UpdateMenuParam
from backend.app.services.service_menu import menu_service
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.common.security.permission import RequestPermission
from backend.app.common.security.rbac import DependsRBAC
from backend.app.utils.serializers import select_as_dict

router = APIRouter()

@router.get('/sidebar', summary='获取用户菜单展示树', dependencies=[DependsJwtAuth])
async def get_user_sidebar_tree(request: Request) -> ResponseModel:
    menu = await menu_service.get_user_menu_tree(request=request)
    return await response_base.success(data=menu)


@router.get('/{pk}', summary='获取菜单详情', dependencies=[DependsJwtAuth])
async def get_menu(pk: Annotated[int, Path(...)]) -> ResponseModel:
    menu = await menu_service.get(pk=pk)
    data = GetMenuListDetails(**await select_as_dict(menu))
    return await response_base.success(data=data)


@router.get('', summary='获取所有菜单展示树', dependencies=[DependsJwtAuth])
async def get_all_menus(
    title: Annotated[Optional[str], Query()] = None, status: Annotated[Optional[int], Query()] = None
) -> ResponseModel:
    menu = await menu_service.get_menu_tree(title=title, status=status)
    return await response_base.success(data=menu)


@router.post('',summary='创建菜单', dependencies=[Depends(RequestPermission('sys:menu:add')), DependsRBAC])
async def create_menu(obj: CreateMenuParam) -> ResponseModel:
    await menu_service.create(obj=obj)
    return await response_base.success()


@router.put('/{pk}',summary='更新菜单', dependencies=[Depends(RequestPermission('sys:menu:edit')), DependsRBAC])
async def update_menu(pk: Annotated[int, Path(...)], obj: UpdateMenuParam) -> ResponseModel:
    count = await menu_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('/{pk}',summary='删除菜单', dependencies=[Depends(RequestPermission('sys:menu:del')), DependsRBAC])
async def delete_menu(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await menu_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()