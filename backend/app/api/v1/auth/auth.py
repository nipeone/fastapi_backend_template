#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/04/15 09:23:37
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks

from backend.app.common.security.jwt import DependsJwtAuth
from backend.app.schemas import GetSwaggerToken, AuthLoginParam, GetLoginToken, GetNewToken
from backend.app.services import auth_service
from backend.app.common.response.response_schema import ResponseModel, response_base

router = APIRouter()

@router.post('/login/swagger', summary='swagger 调试专用', description='用于快捷获取 token 进行 swagger 认证')
async def swagger_login(credentials: Annotated[HTTPBasicCredentials, Depends()]) -> GetSwaggerToken:
    token, user = await auth_service.swagger_login(credentials=credentials)
    return GetSwaggerToken(access_token=token, user=user)  # type: ignore

@router.post(
    '/login', 
    summary="用户登录", 
    description='json 格式登录, 仅支持在第三方api工具调试, 例如: postman',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def user_login(request:Request, obj: AuthLoginParam, background_tasks: BackgroundTasks)->ResponseModel:
    access_token, refresh_token, access_expire, refresh_expire, user = await auth_service.login(request=request, obj=obj, background_tasks=background_tasks)
    data = GetLoginToken(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expire_time=access_expire,
        refresh_token_expire_time=refresh_expire,
        user=user,
    )
    return await response_base.success(data=data)

@router.post('/token/new', summary='创建新 token（刷新token，延长登录）', dependencies=[DependsJwtAuth])
async def create_new_token(request: Request, refresh_token: Annotated[str, Query(...)])->ResponseModel:
    (new_access_token, 
     new_refresh_token, 
     new_access_token_expire_time, 
     new_refresh_token_expire_time) = await auth_service.new_token(request=request, refresh_token=refresh_token)
    data = GetNewToken(
        access_token=new_access_token,
        access_token_expire_time=new_access_token_expire_time,
        refresh_token=new_refresh_token,
        refresh_token_expire_time=new_refresh_token_expire_time,
    )
    return await response_base.success(data=data)

@router.post('/logout', summary='用户登出', dependencies=[DependsJwtAuth])
async def user_logout(request: Request):
    await auth_service.logout(request=request)
    return await response_base.success()