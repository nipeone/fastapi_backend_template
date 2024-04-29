#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_opera_log.py
@Time    :   2024/04/14 12:43:58
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional, Union

from backend.app.common.pagination import paging_data
from backend.app.databases import async_session
from backend.app.crud.crud_opera_log import CRUDOperaLog, opera_log_dao
from backend.app.services.service_base import ServiceBase
from backend.app.models import OperaLog
from backend.app.schemas import CreateOperaLogParam, UpdateOperaLogParam, GetOperaLogListDetails


class ServiceOperaLog(ServiceBase[OperaLog, CreateOperaLogParam, UpdateOperaLogParam]):
    def __init__(self, crud_dao: CRUDOperaLog):
        super().__init__(crud_dao)
        self.crud_dao: CRUDOperaLog

    async def get_pagination(self, *, username: Optional[str] = None, status: Optional[int] = None, ip: Optional[str] = None):
        select_stmt = self.crud_dao.get_select_list(username=username,status=status, ip=ip)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetOperaLogListDetails)
        return page_data

    async def delete_all(self):
        async with async_session.begin() as db:
            count = await self.crud_dao.delete_all(db)
            return count

opera_log_service: ServiceOperaLog = ServiceOperaLog(opera_log_dao)