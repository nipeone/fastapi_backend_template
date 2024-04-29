#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   sys_casbin_rule.py
@Time    :   2024/04/17 10:13:01
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import id_key, MappedBase


class CasbinRule(MappedBase):
    """重写 casbin 中的 CasbinRule model 类, 使用自定义 Base, 避免产生 alembic 迁移问题"""

    __tablename__ = 'sys_casbin_rule'

    id: Mapped[id_key]
    ptype: Mapped[str] = mapped_column(String(255), comment='策略类型: p / g')
    v0: Mapped[str] = mapped_column(String(255), comment='角色ID / 用户uuid')
    v1: Mapped[str] = mapped_column(Text, comment='api路径 / 角色名称')
    v2: Mapped[Optional[str]] = mapped_column(String(255), comment='请求方法')
    v3: Mapped[Optional[str]] = mapped_column(String(255))
    v4: Mapped[Optional[str]] = mapped_column(String(255))
    v5: Mapped[Optional[str]] = mapped_column(String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ', '.join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))