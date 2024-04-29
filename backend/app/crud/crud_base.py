#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2023/12/26 16:14:01
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Select, select, update, delete, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, MappedColumn
from sqlalchemy.sql.elements import BinaryExpression, UnaryExpression, BooleanClauseList, ExpressionClauseList

from backend.app.models.base import Base
from backend.app.common.log import log

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, 
                  db: AsyncSession, 
                  *, 
                  pk: Optional[int] = None, 
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
        assert pk is not None or name is not None, '查询错误, pk 和 name 参数不能同时为空'
        assert pk is None or name is None, '查询错误, pk 和 name 参数不能同时存在'
        where_list = [self.model.id == pk] if pk is not None else [self.model.name == name]
        if status is not None:
            assert status in (0, 1), '查询错误, status 参数只能为 0 或 1'
            where_list.append(self.model.status == status)
        if del_flag is not None:
            assert del_flag in (0, 1), '查询错误, del_flag 参数只能为 0 或 1'
            where_list.append(self.model.del_flag == del_flag)
        result = await db.execute(select(self.model).where(*where_list))
        return result.scalars().one_or_none()
    
    async def single(
            self, 
            db: AsyncSession, 
            *, 
            filters: Optional[Dict[str, Any]] = None
        ) -> Optional[ModelType]:
        """
        通过 filters 过滤条件获取一条数据

        :param db:
        :param filters: 字典类型
        :return:
        """
        se = select(self.model)
        if filters:
            criteria = self.criterionize(filters)
            se = se.where(*criteria)
        result = await db.execute(se)
        return result.scalars().first()

    async def list(
            self, 
            db: AsyncSession, 
            *,
            filters: Union[Dict[Union[str, InstrumentedAttribute], Any], List[Union[BinaryExpression, BooleanClauseList]], None] = None,
            sorts: Optional[List[Union[str, InstrumentedAttribute]]] = None
        ) -> List[ModelType]:
        """
        通过 filters 过滤条件获取列表数据，如果没有过滤条件返回全部数据，慎用

        :param db:
        :param filters: 字典类型
        :return:
        """
        se = select(self.model)
        if sorts:
            orderby = self.criterionize(sorts)
            se = se.order_by(*orderby)
        if filters:
            criteria = self.criterionize(filters)
            se = se.where(*criteria)
        result = await db.execute(se)
        return result.scalars().all()

    async def all(
            self, 
            db: AsyncSession) -> List[ModelType]:
        """
        获取所有数据，没有过滤条件，慎用

        :param db:
        :return:
        """
        se = select(self.model)
        result = await db.execute(se)
        return result.scalars().all()

    def get_select(self,
                *,
               filters: Union[Dict[Union[str, InstrumentedAttribute], Any], List[Union[BinaryExpression, BooleanClauseList]], None] = None,
               sorts: Optional[List[Union[str, InstrumentedAttribute]]] = None)->Select:
        se = select(self.model)
        if sorts:
            orderby = self.criterionize(sorts)
            se = se.order_by(*orderby)
        if filters:
            criteria = self.criterionize(filters)
            se = se.where(*criteria)
        return se

    async def create(
            self, 
            db: AsyncSession,
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
        if user_id:
            create_data = self.model(**obj.model_dump(), create_user=user_id)
        else:
            create_data = self.model(**obj.model_dump())  # type: ignore
        db.add(create_data)
        return create_data

    async def update(
            self, 
            db: AsyncSession,
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
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.model_dump(exclude_unset=True)
        if user_id:
            update_data.update({'update_user': user_id})
        result = await db.execute(update(self.model).where(self.model.id == pk).values(**update_data))
        return result.rowcount

    async def delete(
            self, 
            db: AsyncSession,
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
        del_many = isinstance(pk, list)
        if del_flag is None:
            if del_many:
                result = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
            else:
                result = await db.execute(delete(self.model).where(self.model.id == pk))
        else:
            assert del_flag == 1, '删除错误, del_flag 参数只能为 1'
            if del_many:
                result = await db.execute(update(self.model).where(self.model.id.in_(pk)).values(del_flag=del_flag))
            else:
                result = await db.execute(update(self.model).where(self.model.id == pk).values(del_flag=del_flag))
        return result.rowcount

    def criterionize(self, criterions:Union[List[Union[str, InstrumentedAttribute, BinaryExpression, BooleanClauseList]],Dict[Union[str, InstrumentedAttribute], Any]]) -> List[Any]:
        '''统一 sorts、 filters格式
            criterions
            + example1:
                {'username': 'xxx', 'nickname': 'yyy'}
            + example2:
                {User.username: 'xxx', User.nickname: 'yyy'}
            + example3:
                [User.nickname.like('%x%'),
                User.role_id.in_([1,2]),
                User.nickname.startswith('%x%), 
                not_(User.nickname.like('%x%')),
                and_(User.nickname.like('%x%'), User.role_id.in_([1,2])),
                or_(User.nickname.like('%x%'), User.role_id.in_([1,2]))]
            + example4:
                ['username', 'nickname'] 一般用于sorts排序
            + example5:
                [User.username, User.nickname] 一般用于sorts排序
        
        '''
        cols = self.model.__table__.columns
        rtn=[]
        if isinstance(criterions, dict):
            for c, v in criterions.items():
                if isinstance(c, str):
                    if c in cols:
                        rtn.append(cols[c] == v)
                    else:
                        raise Exception(f"{c} not in {self.model.__tablename__} table")
                elif isinstance(c, (InstrumentedAttribute, MappedColumn)):
                    rtn.append(c == v)
                else:
                    raise Exception(f"unknown column type {type(c)}")

        elif isinstance(criterions, list):
            for c in criterions:
                if isinstance(c, str):
                    if c in cols:
                        rtn.append(cols[c])
                    else:
                        raise Exception(f"{c} not in {self.model.__tablename__} table")
                elif isinstance(c, (InstrumentedAttribute, MappedColumn)):
                    rtn.append(c)
                elif isinstance(c, (BinaryExpression, UnaryExpression, ExpressionClauseList)):
                    rtn.append(c)
        return rtn

