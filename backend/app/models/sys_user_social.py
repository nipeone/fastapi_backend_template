#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   sys_user_social.py
@Time    :   2024/04/17 11:42:54
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key

if TYPE_CHECKING:
    from backend.app.models.sys_user import User


class UserSocial(Base):
    """用户社交表（OAuth2）"""

    __tablename__ = 'sys_user_social'

    id: Mapped[id_key] = mapped_column(init=False)
    source: Mapped[str] = mapped_column(String(20), comment='第三方用户来源')
    open_id: Mapped[Optional[str]] = mapped_column(String(20), default=None, comment='第三方用户的 open id')
    uid: Mapped[Optional[str]] = mapped_column(String(20), default=None, comment='第三方用户的 ID')
    union_id: Mapped[Optional[str]] = mapped_column(String(20), default=None, comment='第三方用户的 union id')
    scope: Mapped[Optional[str]] = mapped_column(String(120), default=None, comment='第三方用户授予的权限')
    code: Mapped[Optional[str]] = mapped_column(String(50), default=None, comment='用户的授权 code')
    # 用户 OAuth2 一对多
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('sys_user.id', ondelete='SET NULL'), default=None, comment='用户关联ID')
    user: Mapped[Optional['User']] = relationship(init=False, back_populates='socials')