#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_opera_log.py
@Time    :   2024/04/14 10:07:09
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional, Union, NoReturn

from sqlalchemy import select, desc, and_, delete, Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import OperaLog
from backend.app.schemas.opera_log import CreateOperaLogParam, UpdateOperaLogParam


class CRUDOperaLog(CRUDBase[OperaLog, CreateOperaLogParam, UpdateOperaLogParam]):
    async def get_select_list(self, 
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

opera_log_dao: CRUDOperaLog = CRUDOperaLog(OperaLog)