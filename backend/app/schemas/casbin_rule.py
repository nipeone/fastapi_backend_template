#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   casbin_rule.py
@Time    :   2024/04/17 10:42:23
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from pydantic import ConfigDict, Field
from backend.app.common.enums import MethodType
from backend.app.schemas.base import SchemaBase


class CreatePolicyParam(SchemaBase):
    sub: str = Field(..., description='用户uuid / 角色ID')
    path: str = Field(..., description='api 路径')
    method: MethodType = Field(default=MethodType.GET, description='请求方法')


class UpdatePolicyParam(CreatePolicyParam):
    pass


class DeletePolicyParam(CreatePolicyParam):
    pass


class DeleteAllPoliciesParam(SchemaBase):
    uuid: Optional[str] = None
    role: str


class CreateUserRoleParam(SchemaBase):
    uuid: str = Field(..., description='用户 uuid')
    role: str = Field(..., description='角色')


class DeleteUserRoleParam(CreateUserRoleParam):
    pass


class GetPolicyListDetails(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ptype: str = Field(..., description='规则类型, p / g')
    v0: str = Field(..., description='用户 uuid / 角色')
    v1: str = Field(..., description='api 路径 / 角色')
    v2: Optional[str] = None
    v3: Optional[str] = None
    v4: Optional[str] = None
    v5: Optional[str] = None
