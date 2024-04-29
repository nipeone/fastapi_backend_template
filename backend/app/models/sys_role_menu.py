#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   sys_role_menu.py
@Time    :   2024/04/17 09:46:51
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.app.models.base import Base

RoleMenu = Table(
    'sys_role_menu',
    Base.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='角色ID'),
    Column('menu_id', Integer, ForeignKey('sys_menu.id', ondelete='CASCADE'), primary_key=True, comment='菜单ID'),
)