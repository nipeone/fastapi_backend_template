#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2023/12/26 17:08:28
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional, Union
from datetime import datetime
from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator

from backend.app.schemas.base import SchemaBase, CustomPhoneNumber
from backend.app.schemas.dept import GetDeptListDetails
from backend.app.schemas.role import GetRoleListDetails
from backend.app.common.enums import StatusType

class AuthSchemaBase(SchemaBase):
    username: str
    password: str


class AuthLoginParam(AuthSchemaBase):
    captcha: str

class RegisterUserSubmissionParam(AuthSchemaBase):
    captcha: str
    nickname: Optional[str] = None
    email: EmailStr = Field(..., example='user@example.com')

class RegisterUserParam(AuthSchemaBase):
    nickname: Optional[str] = None
    email: EmailStr = Field(..., example='user@example.com')
    status: StatusType = Field(default=StatusType.enable)

class RegisterSuperUserParam(RegisterUserParam):
    is_superuser: bool = True


class CreateUserParam(AuthSchemaBase):
    dept_id: int
    roles: list[int]
    nickname: Optional[str] = None
    email: EmailStr = Field(..., example='user@example.com')
    status: StatusType = Field(default=StatusType.enable)

class UserInfoSchemaBase(SchemaBase):
    dept_id: Optional[int] = None
    username: str
    nickname: str
    email: EmailStr = Field(..., example='user@example.com')
    phone: Optional[CustomPhoneNumber] = None

class UpdateUserParam(UserInfoSchemaBase):
    pass

class UpdateUserRoleParam(SchemaBase):
    roles: list[int]

class AvatarParam(SchemaBase):
    url: HttpUrl = Field(..., description='头像 http 地址')

class GetUserInfoNoRelationDetail(UserInfoSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    dept_id: Optional[int] = None
    id: int
    uuid: str
    avatar: Optional[str] = None
    status: StatusType = Field(default=StatusType.enable)
    is_superuser: bool
    join_time: datetime = None
    last_login_time: Optional[datetime] = None


class GetUserInfoListDetails(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)

    dept: Optional[GetDeptListDetails] = None
    roles: list[GetRoleListDetails]


class GetCurrentUserInfoDetail(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)

    dept: Optional[Union[GetDeptListDetails, str]] = None
    roles: Optional[Union[list[GetRoleListDetails], list[str]]] = None

    @model_validator(mode='after')
    def handel(self, values):
        """处理部门和角色"""
        dept = self.dept
        if dept:
            self.dept = dept.name  # type: ignore
        roles = self.roles
        if roles:
            self.roles = [role.name for role in roles]  # type: ignore
        return values

class ResetPasswordParam(SchemaBase):
    old_password: str
    new_password: str
    confirm_password: str