#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   role.py
@Time    :   2024/04/17 10:32:55
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.schemas.base import SchemaBase
from backend.app.schemas.menu import GetMenuListDetails
from backend.app.common.enums import RoleDataScopeType, StatusType

class RoleSchemaBase(SchemaBase):
    name: str
    data_scope: RoleDataScopeType = Field(
        default=RoleDataScopeType.custom, description='权限范围（1：全部数据权限 2：自定义数据权限）'
    )
    status: StatusType = Field(default=StatusType.enable)
    remark: Optional[str] = None

class CreateRoleParam(RoleSchemaBase):
    pass

class UpdateRoleParam(RoleSchemaBase):
    pass

class UpdateRoleMenuParam(SchemaBase):
    menus: list[int]

class GetRoleListDetails(RoleSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
    update_time: Optional[datetime] = None
    menus: list[GetMenuListDetails]