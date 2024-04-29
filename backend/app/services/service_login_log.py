#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_login_log.py
@Time    :   2024/04/14 12:44:35
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime

from fastapi import Request
from sqlalchemy import Select

from backend.app.common.log import log
from backend.app.common.pagination import paging_data
from backend.app.crud.crud_login_log import CRUDLoginLog, login_log_dao
from backend.app.services.service_base import ServiceBase
from backend.app.databases.mysql import async_session
from backend.app.models import LoginLog, User
from backend.app.schemas import CreateLoginLogParam, UpdateLoginLogParam, GetLoginLogListDetails


class ServiceLoginLog((ServiceBase[LoginLog, CreateLoginLogParam, UpdateLoginLogParam])):

    def __init__(self, crud_dao: CRUDLoginLog):
        super().__init__(crud_dao)
        self.crud_dao: CRUDLoginLog

    async def get_pagination(self, *, username: str, status: int, ip: str):
        select_stmt =  self.crud_dao.get_select_list(username=username, status=status, ip=ip)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetLoginLogListDetails)
        return page_data

    async def append(self, 
        *, 
        request: Request, 
        user: User, 
        login_time: datetime, 
        status: int, 
        msg: str
    ) -> LoginLog:
        try:
            # request.state 来自 opera log 中间件定义的扩展参数，详见 opera_log_middleware.py
            async with async_session.begin() as db:
                obj = CreateLoginLogParam(
                    user_uuid=user.uuid,
                    username=user.username,
                    status=status,
                    ip=request.state.ip,
                    country=request.state.country,
                    region=request.state.region,
                    city=request.state.city,
                    user_agent=request.state.user_agent,
                    browser=request.state.browser,
                    os=request.state.os,
                    device=request.state.device,
                    msg=msg,
                    login_time=login_time,
                )
                return await self.crud_dao.create(db, obj=obj)
        except Exception as e:
            log.exception(f'登录日志创建失败: {e}')

    async def delete_all(self) -> int:
        async with async_session.begin() as db:
            count = await self.crud_dao.delete_all(db)
            return count

login_log_service: ServiceLoginLog = ServiceLoginLog(login_log_dao)