#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   sys_menu.py
@Time    :   2024/04/17 09:41:55
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import id_key, Base, SQLIntEnum
from backend.app.models.sys_role_menu import RoleMenu
from backend.app.common.enums import StatusType

if TYPE_CHECKING:
    from backend.app.models.sys_role import Role

class Menu(Base):
    """菜单表"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='菜单标题')
    name: Mapped[str] = mapped_column(String(50), comment='菜单名称')
    level: Mapped[int] = mapped_column(default=0, comment='菜单层级')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    icon: Mapped[Optional[str]] = mapped_column(String(100), default=None, comment='菜单图标')
    path: Mapped[Optional[str]] = mapped_column(String(200), default=None, comment='路由地址')
    menu_type: Mapped[int] = mapped_column(default=0, comment='菜单类型（0目录 1菜单 2按钮）')
    component: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='组件路径')
    perms: Mapped[Optional[str]] = mapped_column(String(100), default=None, comment='权限标识')
    status: Mapped[StatusType] = mapped_column(SQLIntEnum(StatusType), default=StatusType.enable, comment='菜单状态（0停用 1正常）')
    show: Mapped[int] = mapped_column(default=1, comment='是否显示（0否 1是）')
    cache: Mapped[int] = mapped_column(default=1, comment='是否缓存（0否 1是）')
    remark: Mapped[Optional[str]] = mapped_column(Text, default=None, comment='备注')
    # 父级菜单一对多
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('sys_menu.id', ondelete='SET NULL'), default=None, index=True, comment='父菜单ID')
    # **特别注意: 包含自引用的类，id列需要在本类申明，不能继承。
    #   因为如果使用继承的id列，设置remote_side=[id]时会将id识别为内置函数而不是定义的主键列
    # 因为设置了Mapped，可以不用设置uselist=False
    parent: Mapped[Optional['Menu']] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[Optional[list['Menu']]] = relationship(init=False, back_populates='parent')
    # 菜单角色多对多
    roles: Mapped[list['Role']] = relationship(init=False, secondary=RoleMenu, back_populates='menus')