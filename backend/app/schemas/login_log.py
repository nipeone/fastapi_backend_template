#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   login_log.py
@Time    :   2024/04/14 10:07:56
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

from backend.app.schemas.base import SchemaBase

class LoginLogSchemaBase(SchemaBase):
    user_uuid: str
    username: str
    status: int
    ip: str
    country: Optional[str]
    region: Optional[str]
    city: Optional[str]
    user_agent: str
    browser: Optional[str]
    os: Optional[str]
    device: Optional[str]
    msg: str
    login_time: datetime


class CreateLoginLogParam(LoginLogSchemaBase):
    pass


class UpdateLoginLogParam(LoginLogSchemaBase):
    pass


class GetLoginLogListDetails(LoginLogSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
