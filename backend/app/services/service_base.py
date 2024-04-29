#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_base.py
@Time    :   2024/04/14 10:23:35
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from backend.app.models.base import Base
from backend.app.crud.crud_base import CRUDBase
from backend.app.databases.mysql import async_session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class ServiceBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, crud_dao:CRUDBase):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `crud_dao`: A database access object
        """
        self.crud_dao = crud_dao

    async def get(self, 
                  *, 
                  pk: int, 
                  name: Optional[str] = None,
                  status: Optional[str] = None,
                  del_flag: Optional[int] = None,
                  ) -> Optional[ModelType]:
        """
        通过主键 id 或者 name 获取一条数据

        :param db:
        :param pk:
        :param name:
        :param status:
        :param del_flag:
        :return:
        """
        async with async_session() as db:
            return await self.crud_dao.get(db, pk=pk, name=name, status=status, del_flag=del_flag)

    async def single(
            self, 
            *, 
            filters: Optional[Dict[str, Any]] = None
        ) -> Optional[ModelType]:
        async with async_session() as db:
            return await self.crud_dao.single(db, filters=filters)

    async def list(
            self, 
            *,
            filters: Optional[Dict[str, Any]] = None,
            sorts: Optional[Dict[str, Any]] = None
        ) -> List[ModelType]:
        """
        通过 filters 过滤条件获取列表数据，如果没有过滤条件返回全部数据，慎用

        :param db:
        :param filters: 字典类型
        :return:
        """
        async with async_session() as db:
            return await self.crud_dao.list(db, filters=filters,sorts=sorts)

    async def all(self) -> List[ModelType]:
        """
        获取所有数据，没有过滤条件，慎用

        :param db:
        :return:
        """
        async with async_session() as db:
            return await self.crud_dao.all(db)

    def get_select(self,
                   filters: Optional[Dict[Union[str, InstrumentedAttribute], Any]] = None,
                   sorts:Optional[List[Union[str, InstrumentedAttribute]]] = None)->Select:
        return self.crud_dao.get_select(filters=filters, sorts=sorts)


    async def create(
            self, 
            *,
            obj: CreateSchemaType, 
            user_id: Optional[int] = None
        ) -> ModelType:
        """
        新增一条数据

        :param db:
        :param obj: Pydantic 模型类
        :param user_id:
        :return:
        """
        async with async_session.begin() as db:
            return await self.crud_dao.create(db, obj=obj, user_id=user_id)

    async def update(
            self,
            *,
            pk: Any, 
            obj: Union[UpdateSchemaType, Dict[str, Any]], 
            user_id: Optional[int] = None
        ) -> int:
        """
        通过主键 id 更新一条数据

        :param db:
        :param pk:
        :param obj: Pydantic模型类 or 对应数据库字段的字典
        :param user_id:
        :return:
        """
        async with async_session.begin() as db:
            return await self.crud_dao.update(db, pk=pk, obj=obj)
    
    async def delete(
            self,
            *,
            pk: Union[int, List[int]], 
            del_flag: Optional[int] = None
        ) -> int:
        """
        通过主键 id 删除数据

        :param db:
        :param pk:
        :param del_flag:
        :return:
        """
        async with async_session.begin() as db:
            return await self.crud_dao.delete(db, pk=pk, del_flag=del_flag)