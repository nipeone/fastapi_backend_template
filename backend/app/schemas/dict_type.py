#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dict_type.py
@Time    :   2024/04/19 09:09:19
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


class DictTypeSchemaBase(SchemaBase):
    name: str
    code: str
    status: StatusType = Field(default=StatusType.enable)
    remark: Optional[str] = None


class CreateDictTypeParam(DictTypeSchemaBase):
    pass


class UpdateDictTypeParam(DictTypeSchemaBase):
    pass


class GetDictTypeListDetails(DictTypeSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
    update_time: Optional[datetime] = None