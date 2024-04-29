#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_role.py
@Time    :   2024/04/19 16:15:40
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Optional, Sequence
from fastapi import Request

from backend.app.core.conf import settings
from backend.app.common.exception import errors
from backend.app.common.cache.redis import redis_client
from backend.app.common.pagination import paging_data
from backend.app.services.service_base import ServiceBase
from backend.app.models import Role
from backend.app.schemas import CreateRoleParam, UpdateRoleParam, UpdateRoleMenuParam, GetRoleListDetails
from backend.app.databases import async_session
from backend.app.crud import role_dao, menu_dao, CRUDRole


class ServiceRole(ServiceBase[Role, CreateRoleParam, UpdateRoleParam]):
    def __init__(self, crud_dao: CRUDRole):
        super().__init__(crud_dao)
        self.crud_dao: CRUDRole
    
    async def get(self, *, pk: int) -> Role:
        async with async_session() as db:
            role = await self.crud_dao.get_with_relation(db, role_id=pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role
        
    async def get_user_roles(self, *, pk: int) -> Sequence[Role]:
        async with async_session() as db:
            roles = await self.crud_dao.get_user_roles(db, user_id=pk)
            return roles

    async def get_pagination(self, name: str = None, data_scope: int = None, status: int = None):
        select_stmt = self.crud_dao.get_select_list(name=name, data_scope=data_scope, status=status)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetRoleListDetails)
        return page_data

    async def create(self, *, obj: CreateRoleParam) -> None:
        async with async_session.begin() as db:
            role = await self.crud_dao.get_by_name(db, name=obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            await self.crud_dao.create(db, obj=obj)

    async def update(self, *, pk: int, obj: UpdateRoleParam) -> int:
        async with async_session.begin() as db:
            role = await self.crud_dao.get(db, pk=pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            if role.name != obj.name:
                role = await self.crud_dao.get_by_name(db, name=obj.name)
                if role:
                    raise errors.ForbiddenError(msg='角色已存在')
            count = await self.crud_dao.update(db, pk=pk, obj=obj)
            return count
        
    async def update_role_menu(self, *, request: Request, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        async with async_session.begin() as db:
            role = await self.crud_dao.get(db, pk=pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for menu_id in menu_ids.menus:
                menu = await menu_dao.get(db, pk=menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='菜单不存在')
            count = await self.crud_dao.update_menus(db, role_id=pk, menu_ids=menu_ids)
            await redis_client.delete_prefix(f'{settings.PERMISSION_REDIS_PREFIX}:{request.user.uuid}')
            return count
        
role_service = ServiceRole(role_dao)