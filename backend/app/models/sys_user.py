#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/04/13 20:05:02
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.utils.timezone import timezone
from backend.app.models.base import id_key, DataClassBase, uuid4_str, SQLIntEnum
from backend.app.models.sys_user_role import UserRole
from backend.app.common.enums import StatusType

if TYPE_CHECKING:
    from backend.app.models.sys_role import Role
    from backend.app.models.sys_dept import Dept
    from backend.app.models.sys_user_social import UserSocial

class User(DataClassBase):
    '''用户表'''

    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False, comment='用户名')
    nickname: Mapped[Optional[str]] = mapped_column(String(20), comment='昵称')
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码')
    salt: Mapped[Optional[str]] = mapped_column(String(5), comment='加密盐')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment='邮箱')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='超级权限(0否 1是)')
    status: Mapped[StatusType] = mapped_column(SQLIntEnum(StatusType), default=StatusType.enable, comment='用户账号状态(0停用 1启用)')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='头像')
    phone: Mapped[Optional[str]] = mapped_column(String(11), default=None, comment='手机号')
    join_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='注册时间')
    last_login_time: Mapped[Optional[datetime]] = mapped_column(init=False, onupdate=timezone.now, comment='上次登录')
    # 部门用户一对多
    dept_id: Mapped[Optional[int]] = mapped_column(ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, comment='部门关联ID')
    dept: Mapped[Optional['Dept']] = relationship(init=False, back_populates='users')
    # 用户角色多对多
    roles: Mapped[list['Role']] = relationship(init=False, secondary=UserRole, back_populates='users')
    # 用户 OAuth2 一对多
    socials: Mapped[list['UserSocial']] = relationship(init=False, back_populates='user')  # noqa: F821