#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_dict_data.py
@Time    :   2024/04/19 14:34:05
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Optional

from backend.app.common.exception import errors
from backend.app.common.pagination import paging_data
from backend.app.services.service_base import ServiceBase
from backend.app.models import DictData
from backend.app.schemas import CreateDictDataParam, UpdateDictDataParam, GetDictDataListDetails
from backend.app.databases import async_session
from backend.app.crud import dict_data_dao, dict_type_dao, CRUDDictData
from backend.app.utils.build_tree import get_tree_data

class ServiceDictData(ServiceBase[DictData, CreateDictDataParam, UpdateDictDataParam]):

    def __init__(self, crud_dao: CRUDDictData):
        super().__init__(crud_dao)
        self.crud_dao: CRUDDictData

    async def get_pagination(self, *, label: str = None, value: str = None, status: int = None):
        select_stmt = self.crud_dao.get_select_list(label=label, value=value, status=status)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetDictDataListDetails)
        return page_data

    async def create(self, *, obj: CreateDictDataParam) -> DictData:
        async with async_session.begin() as db:
            dict_data = await self.crud_dao.get_by_label(db, label=obj.label)
            if dict_data:
                raise errors.ForbiddenError(msg='字典数据已存在')
            dict_type = await self.crud_dao.get(db, pk=obj.type_id)
            if not dict_type:
                raise errors.ForbiddenError(msg='字典类型不存在')
            return await self.crud_dao.create(db, obj=obj)

    async def update(self, *, pk: int, obj: UpdateDictDataParam) -> int:
        async with async_session.begin() as db:
            dict_data = await self.crud_dao.get(db, pk=pk)
            if not dict_data:
                raise errors.NotFoundError(msg='字典数据不存在')
            if dict_data.label != obj.label:
                if await self.crud_dao.get_by_label(db, label=obj.label):
                    raise errors.ForbiddenError(msg='字典数据已存在')
            dict_type = await dict_type_dao.get(db, pk=obj.type_id)
            if not dict_type:
                raise errors.ForbiddenError(msg='字典类型不存在')
            count = await self.crud_dao.update(db, pk=pk, obj=obj)
            return count
        
    async def delete(self, *, pk: list[int]) -> int:
        async with async_session.begin() as db:
            count = await self.crud_dao.delete(db, pk=pk)
            return count

dict_data_service = ServiceDictData(dict_data_dao)