#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/04/15 15:05:54
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Query, HTTPException, Request, Body, Path, Depends

from backend.app.core.conf import settings
from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.common.security.rbac import DependsRBAC
from backend.app.common.security.permission import RequestPermission
from backend.app.common.pagination import DependsPagination
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.schemas import (
    CreateUserParam, 
    UpdateUserParam,
    UpdateUserRoleParam,
    ResetPasswordParam, 
    RegisterUserSubmissionParam,
    GetCurrentUserInfoDetail,
    GetUserInfoListDetails)
from backend.app.services import user_service
from backend.app.utils.serializers import select_as_dict

router = APIRouter()

@router.post('/register', summary='用户注册')
async def register_user(
    *,
    request: Request,
    obj: RegisterUserSubmissionParam
):
    await user_service.register(request, obj=obj)
    return await response_base.success()


@router.post('/add', summary='添加用户', dependencies=[DependsRBAC])
async def add_user(request: Request, obj: CreateUserParam) -> ResponseModel:
    await user_service.add(request=request, obj=obj)
    current_user = await user_service.get_userinfo(username=obj.username)
    data = GetUserInfoListDetails(**await select_as_dict(current_user))
    return await response_base.success(data=data)

@router.post('/password/reset', summary='密码重置', dependencies=[DependsJwtAuth])
async def password_reset(request: Request, obj: ResetPasswordParam) -> ResponseModel:
    count = await user_service.pwd_reset(request=request, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()

@router.get('/me', summary='获取当前用户信息', dependencies=[DependsJwtAuth], response_model_exclude={'password'})
async def get_current_user(request: Request) -> ResponseModel:
    data = GetCurrentUserInfoDetail(**await select_as_dict(request.user))
    return await response_base.success(data=data)

@router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtAuth])
async def get_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    current_user = await user_service.get_userinfo(username=username)
    data = GetUserInfoListDetails(**await select_as_dict(current_user))
    return await response_base.success(data=data)

@router.put('/{username}', summary='更新用户信息', dependencies=[DependsJwtAuth])
async def update_user(request: Request, username: Annotated[str, Path(...)], obj: UpdateUserParam) -> ResponseModel:
    count = await user_service.update_userinfo(request=request, username=username, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()

@router.put(
    '/{username}/role',
    summary='更新用户角色',
    dependencies=[
        Depends(RequestPermission('sys:user:role:edit')),
        DependsRBAC,
    ],
)
async def update_user_role(
    request: Request, username: Annotated[str, Path(...)], obj: UpdateUserRoleParam
) -> ResponseModel:
    await user_service.update_roles(request=request, username=username, obj=obj)
    return await response_base.success()

@router.get(
    '',
    summary='（模糊条件）分页获取所有用户',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_users(
    dept: Annotated[Optional[int], Query()] = None,
    username: Annotated[Optional[str], Query()] = None,
    phone: Annotated[Optional[str], Query()] = None,
    status: Annotated[Optional[int], Query()] = None,
):
    page_data = await user_service.get_pagination(dept=dept, username=username, phone=phone, status=status)
    return await response_base.success(data=page_data)

@router.delete(
    path='/{username}',
    summary='用户注销',
    description='用户注销 != 用户登出，注销之后用户将从数据库删除',
    dependencies=[
        Depends(RequestPermission('sys:user:del')),
        DependsRBAC,
    ],
)
async def delete_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    count = await user_service.delete_by_username(username=username)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()

