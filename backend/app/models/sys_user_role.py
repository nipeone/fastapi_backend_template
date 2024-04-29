#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user_role.py
@Time    :   2024/04/15 17:18:29
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.app.models.base import Base

UserRole = Table(
    'sys_user_role',
    Base.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('user_id', Integer, ForeignKey('sys_user.id', ondelete='CASCADE'), nullable=False, primary_key=True, comment='用户ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), nullable=False, primary_key=True, comment='角色ID'),
)
