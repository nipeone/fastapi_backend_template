#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   opera_log.py
@Time    :   2024/04/14 10:04:41
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.mysql import JSON, LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import DataClassBase, id_key
from backend.app.utils.timezone import timezone


class OperaLog(DataClassBase):
    """操作日志表"""

    __tablename__ = 'sys_opera_log'

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[Optional[str]] = mapped_column(String(20), comment='用户名')
    method: Mapped[str] = mapped_column(String(20), comment='请求类型')
    title: Mapped[str] = mapped_column(String(255), comment='操作模块')
    path: Mapped[str] = mapped_column(String(500), comment='请求路径')
    ip: Mapped[str] = mapped_column(String(50), comment='IP地址')
    country: Mapped[Optional[str]] = mapped_column(String(50), comment='国家')
    region: Mapped[Optional[str]] = mapped_column(String(50), comment='地区')
    city: Mapped[Optional[str]] = mapped_column(String(50), comment='城市')
    user_agent: Mapped[str] = mapped_column(String(255), comment='请求头')
    os: Mapped[Optional[str]] = mapped_column(String(50), comment='操作系统')
    browser: Mapped[Optional[str]] = mapped_column(String(50), comment='浏览器')
    device: Mapped[Optional[str]] = mapped_column(String(50), comment='设备')
    args: Mapped[Optional[str]] = mapped_column(JSON(), comment='请求参数')
    status: Mapped[int] = mapped_column(comment='操作状态（0异常 1正常）')
    code: Mapped[str] = mapped_column(String(20), insert_default='200', comment='操作状态码')
    msg: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='提示消息')
    cost_time: Mapped[float] = mapped_column(insert_default=0.0, comment='请求耗时ms')
    opera_time: Mapped[datetime] = mapped_column(comment='操作时间')
    create_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='创建时间')
