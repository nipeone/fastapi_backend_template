#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   token.py
@Time    :   2024/04/15 09:24:58
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime

from backend.app.schemas.base import SchemaBase
from backend.app.schemas.user import GetUserInfoNoRelationDetail

class GetSwaggerToken(SchemaBase):
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfoNoRelationDetail

class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime

class GetLoginToken(AccessTokenBase):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime
    user: GetUserInfoNoRelationDetail

class GetNewToken(AccessTokenBase):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime