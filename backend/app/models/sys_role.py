#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   role.py
@Time    :   2024/04/15 17:14:37
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key, SQLIntEnum
from backend.app.models.sys_user_role import UserRole
from backend.app.models.sys_role_menu import RoleMenu
from backend.app.common.enums import StatusType

if TYPE_CHECKING:
    from backend.app.models.sys_user import User
    from backend.app.models.sys_menu import Menu

class Role(Base):
    """角色表"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='角色名称')
    data_scope: Mapped[Optional[int]] = mapped_column(default=2, comment='权限范围（1：全部数据权限 2：自定义数据权限）')
    status: Mapped[StatusType] = mapped_column(SQLIntEnum(StatusType), default=StatusType.enable, comment='角色状态（0停用 1正常）')
    remark: Mapped[Optional[str]] = mapped_column(Text, default=None, comment='备注')
    # 角色用户多对多
    users: Mapped[list['User']] = relationship(init=False, secondary=UserRole, back_populates='roles')
    # 角色菜单多对多
    menus: Mapped[list['Menu']] = relationship(init=False, secondary=RoleMenu, back_populates='roles')