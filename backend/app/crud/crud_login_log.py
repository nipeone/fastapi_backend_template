#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_login_log.py
@Time    :   2024/04/14 10:07:27
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from typing import NoReturn

from sqlalchemy import Select, select, desc, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import LoginLog
from backend.app.schemas.login_log import CreateLoginLogParam, UpdateLoginLogParam


class CRUDLoginLog(CRUDBase[LoginLog, CreateLoginLogParam, UpdateLoginLogParam]):

    def get_select_list(self, 
                        username: Optional[str] = None, 
                        status: Optional[int] = None, 
                        ip: Optional[str] = None) -> Select:
        se = select(self.model).order_by(desc(self.model.create_time))
        where_list = []
        if username:
            where_list.append(self.model.username.like(f'%{username}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if ip:
            where_list.append(self.model.ip.like(f'%{ip}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def delete_all(self, db: AsyncSession) -> int:
        logs = await db.execute(delete(self.model))
        return logs.rowcount

login_log_dao: CRUDLoginLog = CRUDLoginLog(LoginLog)