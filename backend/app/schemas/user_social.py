#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user_social.py
@Time    :   2024/04/19 08:59:50
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from backend.app.common.enums import UserSocialType
from backend.app.schemas.base import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    source: UserSocialType
    open_id: Optional[str] = None
    uid: Optional[str] = None
    union_id: Optional[str] = None
    scope: Optional[str] = None
    code: Optional[str] = None


class CreateUserSocialParam(UserSocialSchemaBase):
    user_id: int


class UpdateUserSocialParam(SchemaBase):
    pass