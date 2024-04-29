#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_user.py
@Time    :   2024/04/13 20:27:11
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any, Dict, Optional, Union

from fast_captcha import text_captcha
from sqlalchemy import Select, select, update, desc, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import User, Role, Dept
from backend.app.schemas.user import (
    CreateUserParam, 
    UpdateUserParam, 
    RegisterUserParam, 
    UpdateUserRoleParam,
    AvatarParam)
from backend.app.common.security import jwt
from backend.app.utils.timezone import timezone


class CRUDUser(CRUDBase[User, CreateUserParam, UpdateUserParam]):
    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        return await self.single(db, filters={User.username: username})
    
    async def get_by_nickname(self, db: AsyncSession, *, nickname: str) -> Optional[User]:
        return await self.single(db, filters={User.nickname: nickname})

    async def register(self, db: AsyncSession, *, obj: RegisterUserParam, social: bool = False) -> User:
        '''注册用户, 如果是第三方授权登录不需要密码'''
        if not social:
            salt = text_captcha(5)
            obj.password = await jwt.get_hash_password(obj.password + salt)
            dict_obj = obj.model_dump()
            dict_obj.update({'salt': salt})
        else:
            dict_obj = obj.model_dump()
            dict_obj.update({'salt': None})
        db_obj = self.model(**dict_obj)  # type: ignore
        db.add(db_obj)
        return db_obj

    async def add(self, db: AsyncSession, *, obj: CreateUserParam) -> User:
        '''后台添加用户'''
        salt = text_captcha(5)
        obj.password = await jwt.get_hash_password(obj.password + salt)
        dict_obj = obj.model_dump(exclude={'roles'})
        dict_obj.update({'salt': salt})
        new_user = self.model(**dict_obj)
        role_list = [await db.get(Role, role_id) for role_id in obj.roles]
        new_user.roles.extend(role_list)
        db.add(new_user)
        return new_user

    async def update_userinfo(self, db: AsyncSession, *, input_user: User, obj: UpdateUserParam) -> int:
        """
        更新用户信息

        :param db:
        :param input_user:
        :param obj:
        :return:
        """
        return await self.update(db, pk = input_user.id, obj=obj)

    async def update_role(self, db: AsyncSession, *, input_user: User, obj: UpdateUserRoleParam) -> None:
        """
        更新用户角色

        :param db:
        :param input_user:
        :param obj:
        :return:
        """
        # 现有角色Id
        cur_role_ids = [r.id for r in input_user.roles]
        # 删除用户角色
        for r in list(input_user.roles):
            if r.id not in obj.roles:
                input_user.roles.remove(r)
        # 添加用户角色
        role_list = []
        for role_id in obj.roles:
            if role_id not in cur_role_ids:
                role_list.append(await db.get(Role, role_id))
        input_user.roles.extend(role_list)

    async def update_avatar(self, db: AsyncSession, *, current_user: User, avatar: AvatarParam) -> int:
        """
        更新用户头像

        :param db:
        :param current_user:
        :param avatar:
        :return:
        """
        user = await db.execute(update(self.model).where(self.model.id == current_user.id).values(avatar=avatar.url))
        return user.rowcount

    async def update_status(self, db: AsyncSession, *, pk:int, status:int):
        ''' ### 更新用户账户状态
            args
            * `db`: AsyncSession
            * `pk`: int
                主键 这里指user_id
            * `status`: int
                用户账户状态
            ---
            returns
            * `success`: int
                更新标志, 0: Failed, 1: Succeeded
        '''
        user = await db.execute(
            update(self.model).where(self.model.id == pk).values(status=status)
        )
        return user.rowcount

    async def update_login_time(self, db: AsyncSession, *, username: str) -> int:
        ''' ### 更新用户登录时间
            args
            * `db`: AsyncSession
            * `username`: str
            ---
            returns
            * `success`: int
                更新标志, 0: Failed, 1: Succeeded

        '''
        user = await db.execute(
            update(self.model).where(self.model.username == username).values(last_login_time=timezone.now())
        )
        return user.rowcount

    async def reset_password(self, db: AsyncSession, *, pk: int, password: str, salt: str) -> int:
        hashed_password = await jwt.get_hash_password(password + salt)
        user = await db.execute(
            update(self.model).where(self.model.id == pk).values(password=hashed_password)
        )
        return user.rowcount
    
    async def check_email(self, db: AsyncSession, email: str) -> Optional[User]:
        return await self.single(db, filters={User.email: email})

    def get_select_list(self, dept: int = None, username: str = None, phone: str = None, status: int = None) -> Select:
        """
        获取用户列表

        :param dept:
        :param username:
        :param phone:
        :param status:
        :return:
        """
        se = (
            select(self.model)
            .options(selectinload(self.model.dept))
            .options(selectinload(self.model.roles).selectinload(Role.menus))
            .order_by(desc(self.model.join_time))
        )
        where_list = []
        if dept:
            where_list.append(self.model.dept_id == dept)
        if username:
            where_list.append(self.model.username.like(f'%{username}%'))
        if phone:
            where_list.append(self.model.phone.like(f'%{phone}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_with_relation(self, db: AsyncSession, *, user_id: int = None, username: str = None) -> Optional[User]:
        """
        获取用户和（部门，角色，菜单）

        :param db:
        :param user_id:
        :param username:
        :return:
        """
        criterias = []
        if user_id:
            criterias.append(self.model.id == user_id)
        if username:
            criterias.append(self.model.username == username)
        user = await db.execute(
            select(self.model)
            .options(selectinload(self.model.dept))
            .options(selectinload(self.model.roles).joinedload(Role.menus))
            .where(*criterias)
        )
        return user.scalars().first()

user_dao:CRUDUser = CRUDUser(User)