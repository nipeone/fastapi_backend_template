#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_user.py
@Time    :   2023/12/27 11:33:06
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Dict, Optional, Union
import random
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from backend.app.core.conf import settings
from backend.app.common.exception import errors
from backend.app.common.cache import redis_client
from backend.app.common.security import jwt
from backend.app.common.log import log
from backend.app.common.pagination import paging_data
from backend.app.common.response.response_code import CustomErrorCode
from backend.app.services.service_base import ServiceBase
from backend.app.models import User
from backend.app.schemas import (
    CreateUserParam, 
    UpdateUserParam,
    UpdateUserRoleParam,
    ResetPasswordParam, 
    RegisterUserParam,
    RegisterUserSubmissionParam, 
    GetUserInfoListDetails)
from backend.app.crud import user_dao, role_dao, dept_dao, CRUDUser
from backend.app.databases import async_session



class ServiceUser(ServiceBase[User, CreateUserParam, UpdateUserParam]):
    def __init__(self, crud_dao: CRUDUser):
        super().__init__(crud_dao)
        self.crud_dao: CRUDUser

    async def register(self, request: Request, *, obj: RegisterUserSubmissionParam) -> Optional[User]:
        if not settings.USERS_OPEN_REGISTRATION:
            raise errors.ForbiddenError(msg="未开放注册")
        async with async_session.begin() as db:
            if not obj.password:
                raise errors.ForbiddenError(msg='密码为空')
            captcha_code = await redis_client.get(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
            if not captcha_code:
                raise errors.AuthorizationError(msg='验证码失效，请重新获取')
            if captcha_code.lower() != obj.captcha.lower():
                raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
            user = await self.crud_dao.get_by_username(db, username=obj.username)
            if user:
                raise errors.ForbiddenError(msg="该用户名已注册")
            email = await self.crud_dao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            obj.nickname = obj.nickname if obj.nickname else f'用户{random.randrange(10000, 99999)}'
            _obj = RegisterUserParam(username=obj.username,
                            nickname=obj.nickname,
                            email=obj.email,
                            password=obj.password)
            registered_user = await self.crud_dao.register(db, obj=_obj)
        return registered_user

    async def add(self, *, request: Request, obj: CreateUserParam):
        async with async_session.begin() as db:
            if not obj.password:
                raise errors.ForbiddenError(msg='密码为空')
            await jwt.superuser_verify(request)
            username = await self.crud_dao.get_by_username(db, username=obj.username)
            if username:
                raise errors.ForbiddenError(msg='此用户名已注册')
            obj.nickname = obj.nickname if obj.nickname else f'用户{random.randrange(10000, 99999)}'
            email = await self.crud_dao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            dept = await dept_dao.get(db, pk=obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await role_dao.get(db, pk=role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await self.crud_dao.add(db, obj=obj)


    async def get_by_username(self, *, username: str) -> Optional[User]:
        async with async_session() as db:
            return await self.crud_dao.get_by_username(db, username=username)
        
    async def get_by_nickname(self, *, username: str) -> Optional[User]:
        async with async_session() as db:
            return await self.crud_dao.get_by_nickname(db, username=username)

    async def authenticate(self, *, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(username=username)
        if not user:
            raise errors.NotFoundError(msg='用户不存在')
        if not await jwt.verify_password(password + user.salt, user.password):
            raise errors.AuthorizationError(msg='密码错误')
        if not user.status:
            raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
        return user

    async def update_userinfo(self, *, request: Request, username: str, obj: UpdateUserParam) -> int:
        async with async_session.begin() as db:
            if not request.user.is_superuser and request.user.username != username:
                raise errors.ForbiddenError(msg="只能修改本人信息")
            input_user = await self.crud_dao.get_by_username(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            if input_user.username != obj.username and obj.username is not None:
                _username = await self.crud_dao.get_by_username(db, username=obj.username)
                if _username:
                    raise errors.ForbiddenError(msg='该用户名已存在')
            if input_user.nickname != obj.nickname and obj.nickname is not None:
                nickname = await self.crud_dao.get_by_nickname(db, nickname=obj.nickname)
                if nickname:
                    raise errors.ForbiddenError(msg='该昵称已存在')
            if input_user.email != obj.email and obj.email is not None:
                email = await self.crud_dao.check_email(db, obj.email)
                if email:
                    raise errors.ForbiddenError(msg='该邮箱已注册')
            count = await self.crud_dao.update_userinfo(db, pk=input_user.id, obj=obj)
            return count

    async def get_userinfo(self, *, username: str) -> User:
        async with async_session() as db:
            user = await self.crud_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    async def update_status(self, *, request: Request, pk: int, status:int) -> int:
        async with async_session.begin() as db:
            await jwt.superuser_verify(request)
            if not await self.crud_dao.get(db, pk=pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='禁止修改自身状态')
                count = await self.crud_dao.update_status(db, pk=pk, status=status)
                return count

    async def update_roles(self, *, request: Request, username: str, obj: UpdateUserRoleParam) -> None:
        async with async_session.begin() as db:
            if not request.user.is_superuser:
                if request.user.username != username:
                    raise errors.ForbiddenError(msg='只能修改本人的角色')
            input_user = await self.crud_dao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            for role_id in obj.roles:
                role = await role_dao.get(db, pk=role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await self.crud_dao.update_role(db, input_user=input_user, obj=obj)
            await redis_client.delete_prefix(f'{settings.PERMISSION_REDIS_PREFIX}:{request.user.uuid}')

    async def pwd_reset(self, *, request: Request, obj: ResetPasswordParam) -> int:
        async with async_session.begin() as db:
            op = obj.old_password
            if not await jwt.verify_password(op + request.user.salt, request.user.password):
                raise errors.ForbiddenError(msg='旧密码错误')
            np1 = obj.new_password
            np2 = obj.confirm_password
            if np1 != np2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            count = await self.crud_dao.reset_password(db, request.user.id, obj.new_password, request.user.salt)
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count


    async def get_pagination(self, *, dept:int, username: Optional[str] = None, phone: Optional[str] = None, status: Optional[int] = None):
        select_stmt = self.crud_dao.get_select_list(dept=dept, username=username, phone=phone, status=status)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetUserInfoListDetails)
        return page_data
    
    async def delete_by_username(self, *, username: str) -> int:
        async with async_session.begin() as db:
            input_user = await user_dao.get_by_username(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await user_dao.delete(db, pk=input_user.id)
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{input_user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{input_user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count

user_service: ServiceUser = ServiceUser(user_dao)