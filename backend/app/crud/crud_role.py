#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_role.py
@Time    :   2024/04/17 10:32:03
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Dict, Optional, Union, Sequence

from fast_captcha import text_captcha
from sqlalchemy import Select, select, update, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import User, Role, Menu
from backend.app.schemas.role import CreateRoleParam, UpdateRoleParam, UpdateRoleMenuParam
from backend.app.common.security import jwt
from backend.app.utils.timezone import timezone


class CRUDRole(CRUDBase[Role, CreateRoleParam, UpdateRoleParam]):
    async def get_with_relation(self, db: AsyncSession, *, role_id: int) -> Optional[Role]:
        """
        获取角色和菜单

        :param db:
        :param role_id:
        :return:
        """
        role = await db.execute(
            select(self.model).options(selectinload(self.model.menus)).where(self.model.id == role_id)
        )
        return role.scalars().first()
    
    async def get_user_roles(self, db: AsyncSession, *, user_id: int) -> Sequence[Role]:
        """
        获取用户所有角色

        :param db:
        :param user_id:
        :return:
        """
        roles = await db.execute(select(self.model).join(self.model.users).where(User.id == user_id))
        return roles.scalars().all()

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Role]:
        """
        通过 name 获取角色

        :param db:
        :param name:
        :return:
        """
        role = await db.execute(select(self.model).where(self.model.name == name))
        return role.scalars().first()

    def get_select_list(self, name: str = None, data_scope: int = None, status: int = None) -> Select:
        """
        获取角色列表

        :param name:
        :param data_scope:
        :param status:
        :return:
        """
        se = select(self.model).options(selectinload(self.model.menus)).order_by(desc(self.model.create_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if data_scope:
            where_list.append(self.model.data_scope == data_scope)
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(*where_list)
        return se

    async def update_menus(self, db: AsyncSession, *, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param db:
        :param role_id:
        :param menu_ids:
        :return:
        """
        current_role = await self.get_with_relation(db, role_id=role_id)
        # 更新菜单
        menus = await db.execute(select(Menu).where(Menu.id.in_(menu_ids.menus)))
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)
    
role_dao: CRUDRole = CRUDRole(Role)