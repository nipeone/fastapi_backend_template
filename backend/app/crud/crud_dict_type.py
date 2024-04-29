#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_dict_type.py
@Time    :   2024/04/19 09:12:00
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from sqlalchemy import Select, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import DictType
from backend.app.schemas.dict_type import CreateDictTypeParam, UpdateDictTypeParam

class CRUDDictType(CRUDBase[DictType, CreateDictTypeParam, UpdateDictTypeParam]):

    async def get_select_list(self, *, name: str = None, code: str = None, status: int = None) -> Select:
        """
        获取所有字典类型

        :param name:
        :param code:
        :param status:
        :return:
        """
        se = select(self.model).order_by(desc(self.model.create_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if code:
            where_list.append(self.model.code.like(f'%{code}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(*where_list)
        return se

    async def get_by_code(self, db: AsyncSession, *, code: str) -> Optional[DictType]:
        """
        通过 code 获取字典类型

        :param db:
        :param code:
        :return:
        """
        dept = await db.execute(select(self.model).where(self.model.code == code))
        return dept.scalars().first()
    
dict_type_dao: CRUDDictType = CRUDDictType(DictType)