#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dept.py
@Time    :   2024/04/17 11:02:25
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, Field

from backend.app.common.enums import StatusType
from backend.app.schemas.base import CustomEmailStr, CustomPhoneNumber, SchemaBase


class DeptSchemaBase(SchemaBase):
    name: str
    parent_id: Optional[int] = Field(default=None, description='部门父级ID')
    sort: int = Field(default=0, ge=0, description='排序')
    leader: Optional[str] = None
    phone: Optional[CustomPhoneNumber] = None
    email: Optional[CustomEmailStr] = None
    status: StatusType = Field(default=StatusType.enable)


class CreateDeptParam(DeptSchemaBase):
    pass


class UpdateDeptParam(DeptSchemaBase):
    pass


class GetDeptListDetails(DeptSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    del_flag: bool
    create_time: datetime
    update_time: Optional[datetime] = None