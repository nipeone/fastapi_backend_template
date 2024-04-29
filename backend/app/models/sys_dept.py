#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   sys_dept.py
@Time    :   2024/04/17 10:17:37
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import id_key, Base, SQLIntEnum
from backend.app.common.enums import StatusType

if TYPE_CHECKING:
    from backend.app.models.sys_user import User


class Dept(Base):
    """部门表"""

    __tablename__ = 'sys_dept'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='部门名称')
    level: Mapped[int] = mapped_column(default=0, comment='部门层级')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    leader: Mapped[Optional[str]] = mapped_column(String(20), default=None, comment='负责人')
    phone: Mapped[Optional[str]] = mapped_column(String(11), default=None, comment='手机')
    email: Mapped[Optional[str]] = mapped_column(String(50), default=None, comment='邮箱')
    status: Mapped[StatusType] = mapped_column(SQLIntEnum(StatusType), default=StatusType.enable, comment='部门状态(0停用 1正常)')
    del_flag: Mapped[bool] = mapped_column(default=False, comment='删除标志（0删除 1存在）')
    # 父级部门一对多
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, index=True, comment='父部门ID')
    # **特别注意: 包含自引用的类，id列需要在本类申明，不能继承。
    #   因为如果使用继承的id列，设置remote_side=[id]时会将id识别为内置函数而不是定义的主键列
    parent: Mapped[Optional['Dept']] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[Optional[list['Dept']]] = relationship(init=False, back_populates='parent')
    # 部门用户一对多
    users: Mapped[list['User']] = relationship(init=False, back_populates='dept')  # noqa: F821