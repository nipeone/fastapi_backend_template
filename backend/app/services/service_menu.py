#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_menu.py
@Time    :   2024/04/19 15:54:29
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Optional
from fastapi import Request

from backend.app.core.conf import settings
from backend.app.common.exception import errors
from backend.app.common.cache.redis import redis_client
from backend.app.services.service_base import ServiceBase
from backend.app.models import Menu
from backend.app.schemas import CreateMenuParam, UpdateMenuParam
from backend.app.databases import async_session
from backend.app.crud import menu_dao, role_dao, CRUDMenu
from backend.app.utils.build_tree import get_tree_data


class ServiceMenu(ServiceBase[Menu, CreateMenuParam, UpdateMenuParam]):
    def __init__(self, crud_dao: CRUDMenu):
        super().__init__(crud_dao)
        self.crud_dao: CRUDMenu

    async def get_menu_tree(self, *, title: Optional[str] = None, status: Optional[int] = None) -> list[dict[str, Any]]:
        async with async_session() as db:
            menu_select = await self.crud_dao.get_all(db, title=title, status=status)
            menu_tree = await get_tree_data(menu_select)
            return menu_tree
        
    async def get_role_menu_tree(self, *, pk: int) -> list[dict[str, Any]]:
        async with async_session() as db:
            role = await role_dao.get_with_relation(db, role_id=pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            menu_ids = [menu.id for menu in role.menus]
            menu_select = await self.crud_dao.get_role_menus(db, superuser=False, menu_ids=menu_ids)
            menu_tree = await get_tree_data(menu_select)
            return menu_tree
        
    async def get_user_menu_tree(self, *, request: Request) -> list[dict[str, Any]]:
        async with async_session() as db:
            roles = request.user.roles
            menu_ids = []
            menu_tree = []
            if roles:
                for role in roles:
                    menu_ids.extend([menu.id for menu in role.menus])
                menu_select = await self.crud_dao.get_role_menus(db, superuser=request.user.is_superuser, menu_ids=menu_ids)
                menu_tree = await get_tree_data(menu_select)
            return menu_tree
        
    async def create(self, *, obj: CreateMenuParam) -> Menu:
        async with async_session.begin() as db:
            title = await self.crud_dao.get_by_title(db, title=obj.title)
            if title:
                raise errors.ForbiddenError(msg='菜单标题已存在')
            if obj.parent_id:
                parent_menu = await self.crud_dao.get(db, pk=obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='父级菜单不存在')
            return await self.crud_dao.create(db, obj=obj)
        
    async def update(self, *, pk: int, obj: UpdateMenuParam) -> int:
        async with async_session.begin() as db:
            menu = await self.crud_dao.get(db, pk=pk)
            if not menu:
                raise errors.NotFoundError(msg='菜单不存在')
            if menu.title != obj.title:
                if await self.crud_dao.get_by_title(db, title=obj.title):
                    raise errors.ForbiddenError(msg='菜单标题已存在')
            if obj.parent_id:
                parent_menu = await self.crud_dao.get(db, pk=obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='父级菜单不存在')
            if obj.parent_id == menu.id:
                raise errors.ForbiddenError(msg='禁止关联自身为父级')
            count = await self.crud_dao.update(db, pk=pk, obj=obj)
            await redis_client.delete_prefix(settings.PERMISSION_REDIS_PREFIX)
            return count
        
    async def delete(self, *, pk: int) -> int:
        async with async_session.begin() as db:
            children = await self.crud_dao.get_children(db, menu_id=pk)
            if children:
                raise errors.ForbiddenError(msg='菜单下存在子菜单，无法删除')
            count = await self.crud_dao.delete(db, pk=pk)
            return count
        
menu_service = ServiceMenu(menu_dao)