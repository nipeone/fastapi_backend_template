#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dict_data.py
@Time    :   2024/04/19 09:08:48
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, Field

from backend.app.schemas.dict_type import GetDictTypeListDetails
from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase


class DictDataSchemaBase(SchemaBase):
    type_id: int
    label: str
    value: str
    sort: int
    status: StatusType = Field(default=StatusType.enable)
    remark: Optional[str] = None


class CreateDictDataParam(DictDataSchemaBase):
    pass


class UpdateDictDataParam(DictDataSchemaBase):
    pass


class GetDictDataListDetails(DictDataSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: GetDictTypeListDetails
    create_time: datetime
    update_time: Optional[datetime] = None