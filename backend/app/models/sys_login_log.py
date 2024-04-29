#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   login_log.py
@Time    :   2024/04/14 10:04:17
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import DataClassBase, id_key
from backend.app.utils.timezone import timezone


class LoginLog(DataClassBase):
    """登录日志表"""

    __tablename__ = 'sys_login_log'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(String(50), comment='用户UUID')
    username: Mapped[str] = mapped_column(String(20), comment='用户名')
    status: Mapped[int] = mapped_column(insert_default=0, comment='登录状态(0失败 1成功)')
    ip: Mapped[str] = mapped_column(String(50), comment='登录IP地址')
    country: Mapped[Optional[str]] = mapped_column(String(50), comment='国家')
    region: Mapped[Optional[str]] = mapped_column(String(50), comment='地区')
    city: Mapped[Optional[str]] = mapped_column(String(50), comment='城市')
    user_agent: Mapped[str] = mapped_column(String(255), comment='请求头')
    os: Mapped[Optional[str]] = mapped_column(String(50), comment='操作系统')
    browser: Mapped[Optional[str]] = mapped_column(String(50), comment='浏览器')
    device: Mapped[Optional[str]] = mapped_column(String(50), comment='设备')
    msg: Mapped[str] = mapped_column(LONGTEXT, comment='提示消息')
    login_time: Mapped[datetime] = mapped_column(comment='登录时间')
    create_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='创建时间')
