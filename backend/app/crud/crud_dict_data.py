#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_dict_data.py
@Time    :   2024/04/19 09:16:24
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models import DictData
from backend.app.schemas.dict_data import CreateDictDataParam, UpdateDictDataParam
from backend.app.crud.crud_base import CRUDBase


class CRUDDictData(CRUDBase[DictData, CreateDictDataParam, UpdateDictDataParam]):

    async def get_by_label(self, db: AsyncSession, *, label: str) -> Optional[DictData]:
        """
        通过 label 获取字典数据

        :param db:
        :param label:
        :return:
        """
        api = await db.execute(select(self.model).where(self.model.label == label))
        return api.scalars().first()
    
    def get_select_list(self, label: str = None, value: str = None, status: int = None) -> Select:
        """
        获取所有字典数据

        :param label:
        :param value:
        :param status:
        :return:
        """
        se = select(self.model).options(selectinload(self.model.type)).order_by(desc(self.model.sort))
        where_list = []
        if label:
            where_list.append(self.model.label.like(f'%{label}%'))
        if value:
            where_list.append(self.model.value.like(f'%{value}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_with_relation(self, db: AsyncSession, pk: int) -> Optional[DictData]:
        """
        获取字典数据和类型

        :param db:
        :param pk:
        :return:
        """
        where = [self.model.id == pk]
        dict_data = await db.execute(select(self.model).options(selectinload(self.model.type)).where(*where))
        return dict_data.scalars().first()
    
dict_data_dao: CRUDDictData = CRUDDictData(DictData)