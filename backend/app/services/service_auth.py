#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_auth.py
@Time    :   2024/04/15 09:31:38
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Tuple
from datetime import datetime
from fastapi import Request
from fastapi.security import HTTPBasicCredentials
from starlette.background import BackgroundTasks, BackgroundTask

from backend.app.core.conf import settings
from backend.app.common.enums import LoginLogStatusType
from backend.app.common.security import jwt
from backend.app.common.exception import errors
from backend.app.common.cache.redis import redis_client
from backend.app.common.response.response_code import CustomErrorCode
from backend.app.services.service_base import ServiceBase
from backend.app.crud.crud_user import CRUDUser, user_dao
from backend.app.services.service_login_log import login_log_service
from backend.app.models import User
from backend.app.schemas import AuthLoginParam, CreateUserParam, UpdateUserParam
from backend.app.databases.mysql import async_session
from backend.app.utils.timezone import timezone

class ServiceAuth(ServiceBase[User, CreateUserParam, UpdateUserParam]):

    def __init__(self, crud_dao: CRUDUser):
        super().__init__(crud_dao)
        self.crud_dao: CRUDUser

    async def swagger_login(self, *, credentials: HTTPBasicCredentials):
        async with async_session.begin() as db:
            current_user = await self.crud_dao.get_by_username(db, username=credentials.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not await jwt.verify_password(credentials.password + current_user.salt, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.status:
                raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
            # 创建token
            access_token, _ = await jwt.create_access_token(str(current_user.id))
            # 更新登陆时间
            await self.crud_dao.update_login_time(db, username=credentials.username)
            return access_token, current_user

    async def login(self, *, request: Request, obj: AuthLoginParam, background_tasks: BackgroundTasks)->Tuple[str, str, datetime, datetime, User]:
        async with async_session.begin() as db:
            try:
                current_user = await self.crud_dao.get_by_username(db, username=obj.username)
                if not current_user:
                    raise errors.NotFoundError(msg='用户不存在')
                elif not await jwt.verify_password(obj.password + current_user.salt, current_user.password):
                    raise errors.AuthorizationError(msg='密码错误')
                elif not current_user.status:
                    raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
                captcha_code = await redis_client.get(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                if not captcha_code:
                    raise errors.AuthorizationError(msg='验证码失效，请重新获取')
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                access_token, access_token_expire_time = await jwt.create_access_token(
                    str(current_user.id))
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(current_user.id), access_token_expire_time)
                await self.crud_dao.update_login_time(db, username=obj.username)
                await db.refresh(current_user)
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                err_log_info = dict(
                    request=request,
                    user=current_user,
                    login_time=timezone.now(),
                    status=LoginLogStatusType.fail.value,
                    msg=e.msg,
                )
                task = BackgroundTask(login_log_service.append, **err_log_info)
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                raise e
            else:
                login_log = dict(
                    request=request,
                    user=current_user,
                    login_time=timezone.now(),
                    status=LoginLogStatusType.success.value,
                    msg='登录成功',
                )
                background_tasks.add_task(login_log_service.append, **login_log)
                await redis_client.delete(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                return access_token, refresh_token, access_token_expire_time, refresh_token_expire_time, current_user

    async def new_token(self, *, request: Request, refresh_token: str) -> Tuple[str, str, datetime, datetime]:
        user_id = await jwt.jwt_decode(refresh_token)
        if request.user.id != user_id:
            raise errors.TokenError(msg='刷新 token 无效')
        async with async_session() as db:
            current_user = await self.crud_dao.get(db, pk=user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not current_user.status:
                raise errors.AuthorizationError(msg='用户已锁定，操作失败')
            current_token = await jwt.get_token(request)
            data = await jwt.create_new_token(current_user.id, current_token, refresh_token)
            return data

    async def logout(self, *, request: Request):
        token = await jwt.get_token(request)
        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:'
        await redis_client.delete_prefix(prefix)

auth_service = ServiceAuth(user_dao)