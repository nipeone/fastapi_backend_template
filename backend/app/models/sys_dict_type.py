#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   sys_dict_type.py
@Time    :   2024/04/19 09:05:04
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key, SQLIntEnum
from backend.app.common.enums import StatusType

if TYPE_CHECKING:
    from backend.app.models.sys_dict_data import DictData


class DictType(Base):
    """字典类型"""

    __tablename__ = 'sys_dict_type'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(32), unique=True, comment='字典类型名称')
    code: Mapped[str] = mapped_column(String(32), unique=True, comment='字典类型编码')
    status: Mapped[StatusType] = mapped_column(SQLIntEnum(StatusType), default=StatusType.enable, comment='状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    # 字典类型一对多
    datas: Mapped[list['DictData']] = relationship(init=False, back_populates='type')