#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_dict_type.py
@Time    :   2024/04/19 14:35:13
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Optional

from backend.app.common.exception import errors
from backend.app.common.pagination import paging_data
from backend.app.services.service_base import ServiceBase
from backend.app.models import DictType
from backend.app.schemas import CreateDictTypeParam, UpdateDictTypeParam, GetDictTypeListDetails
from backend.app.databases import async_session
from backend.app.crud import dict_type_dao, CRUDDictType

class ServiceDictType(ServiceBase[DictType, CreateDictTypeParam, UpdateDictTypeParam]):
    
    def __init__(self, crud_dao: CRUDDictType):
        super().__init__(crud_dao)
        self.crud_dao: CRUDDictType
    
    async def get_pagination(self, *, name: str = None, code: str = None, status: int = None):
        select_stmt = self.crud_dao.get_select_list(name=name, code=code, status=status)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetDictTypeListDetails)
        return page_data

    async def create(self, *, obj: CreateDictTypeParam):
        async with async_session.begin() as db:
            dict_type = await self.crud_dao.get_by_code(db, obj.code)
            if dict_type:
                raise errors.ForbiddenError(msg='字典类型已存在')
            return await self.crud_dao.create(db, obj=obj)

    async def update(self, *, pk: int, obj: UpdateDictTypeParam) -> int:
        async with async_session.begin() as db:
            dict_type = await self.crud_dao.get(db, pk=pk)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            if dict_type.code != obj.code:
                if await self.crud_dao.get_by_code(db, obj.code):
                    raise errors.ForbiddenError(msg='字典类型已存在')
            count = await self.crud_dao.update(db, pk=pk, obj=obj)
            return count
        
    async def delete(self, *, pk: list[int]) -> int:
        async with async_session.begin() as db:
            count = await self.crud_dao.delete(db, pk=pk)
            return count

dict_type_service = ServiceDictType(dict_type_dao)