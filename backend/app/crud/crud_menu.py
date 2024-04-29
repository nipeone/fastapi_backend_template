#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_menu.py
@Time    :   2024/04/17 10:52:52
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Dict, Optional, Union, Sequence

from fast_captcha import text_captcha
from sqlalchemy import Select, select, update, desc, asc, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import User, Role, Menu
from backend.app.schemas.menu import CreateMenuParam, UpdateMenuParam
from backend.app.common.security import jwt
from backend.app.utils.timezone import timezone


class CRUDMenu(CRUDBase[Menu, CreateMenuParam, UpdateMenuParam]):

    async def get_by_title(self, db: AsyncSession, *, title: str) -> Optional[Menu]:
        """
        通过 title 获取菜单

        :param db:
        :param title:
        :return:
        """
        result = await db.execute(select(self.model).where(and_(self.model.title == title, self.model.menu_type != 2)))
        return result.scalars().first()
    
    async def get_all(self, 
                      db:AsyncSession, 
                      *, 
                      title: Optional[str] = None, 
                      status: Optional[int] = None) -> Sequence[Menu]:
        """
        获取所有菜单

        :param db:
        :param title:
        :param status:
        :return:
        """
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = []
        if title:
            where_list.append(self.model.title.like(f'%{title}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        menu = await db.execute(se)
        return menu.scalars().all()

    async def get_role_menus(self, db: AsyncSession, *, superuser: bool, menu_ids: list[int]) -> Sequence[Menu]:
        """
        获取角色菜单

        :param db:
        :param superuser:
        :param menu_ids:
        :return:
        """
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = [self.model.menu_type.in_([0, 1])]
        if not superuser:
            where_list.append(self.model.id.in_(menu_ids))
        se = se.where(and_(*where_list))
        menu = await db.execute(se)
        return menu.scalars().all()
    
    async def get_children(self, db:AsyncSession , *, menu_id: int) -> list[Menu]:
        """
        获取子菜单

        :param db:
        :param menu_id:
        :return:
        """
        result = await db.execute(
            select(self.model).options(selectinload(self.model.children)).where(self.model.id == menu_id)
        )
        menu = result.scalars().first()
        return menu.children
    
menu_dao: CRUDMenu = CRUDMenu(Menu)