#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   opera_log.py
@Time    :   2024/04/14 10:08:18
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, Field

from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase


class OperaLogSchemaBase(SchemaBase):
    username: Optional[str] = None
    method: str
    title: str
    path: str
    ip: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    user_agent: str
    os: Optional[str] = None
    browser: Optional[str] = None
    device: Optional[str] = None
    args: Optional[dict] = None
    status: StatusType = Field(default=StatusType.enable)
    code: str
    msg: Optional[str] = None
    cost_time: float
    opera_time: datetime


class CreateOperaLogParam(OperaLogSchemaBase):
    pass


class UpdateOperaLogParam(OperaLogSchemaBase):
    pass


class GetOperaLogListDetails(OperaLogSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime