#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_dept.py
@Time    :   2024/04/19 11:30:20
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Optional

from backend.app.common.exception import errors
from backend.app.services.service_base import ServiceBase
from backend.app.models import Dept
from backend.app.schemas import CreateDeptParam, UpdateDeptParam
from backend.app.databases import async_session
from backend.app.crud import dept_dao, CRUDDept
from backend.app.utils.build_tree import get_tree_data

class ServiceDept(ServiceBase[Dept, CreateDeptParam, UpdateDeptParam]):

    def __init__(self, crud_dao: CRUDDept):
        super().__init__(crud_dao)
        self.crud_dao: CRUDDept

    async def get_dept_tree(self,
        *, name: Optional[str] = None, leader: Optional[str] = None, phone: Optional[str] = None, status: Optional[int] = None) -> list[dict[str, Any]]:
        async with async_session() as db:
            depts = await self.crud_dao.get_all(db, name=name, leader=leader, phone=phone, status=status)
            tree_data = await get_tree_data(depts)
            return tree_data
        
    async def create(self, *, obj: CreateDeptParam) -> None:
        async with async_session.begin() as db:
            dept = await self.crud_dao.get_by_name(db, name=obj.name)
            if dept:
                raise errors.ForbiddenError(msg='部门名称已存在')
            if obj.parent_id:
                parent_dept = await self.crud_dao.get(db, pk=obj.parent_id)
                if not parent_dept:
                    raise errors.NotFoundError(msg='父级部门不存在')
            await self.crud_dao.create(db, obj=obj)

    async def update(self, *, dept_id: int, obj: UpdateDeptParam) -> int:
        async with async_session.begin() as db:
            dept = await self.crud_dao.get(db, pk=dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            if dept.name != obj.name:
                if await self.crud_dao.get_by_name(db, name=obj.name):
                    raise errors.ForbiddenError(msg='部门名称已存在')
            if obj.parent_id:
                parent_dept = await self.crud_dao.get(db, pk=obj.parent_id)
                if not parent_dept:
                    raise errors.NotFoundError(msg='父级部门不存在')
            if obj.parent_id == dept.id:
                raise errors.ForbiddenError(msg='禁止关联自身为父级')
            count = await self.crud_dao.update(db, pk=dept_id, obj=obj)
            return count
        
    async def delete(self, *, dept_id: int) -> int:
        async with async_session.begin() as db:
            dept_user = await self.crud_dao.get_with_relation(db, dept_id=dept_id)
            if dept_user:
                raise errors.ForbiddenError(msg='部门下存在用户，无法删除')
            children = await self.crud_dao.get_children(db, dept_id=dept_id)
            if children:
                raise errors.ForbiddenError(msg='部门下存在子部门，无法删除')
            count = await self.crud_dao.delete(db, pk=dept_id)
            return count
        
dept_service = ServiceDept(dept_dao)