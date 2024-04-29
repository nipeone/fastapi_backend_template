#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   menu.py
@Time    :   2024/04/17 10:33:44
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.schemas.base import SchemaBase
from backend.app.common.enums import MenuType, StatusType

class MenuSchemaBase(SchemaBase):
    title: str
    name: str
    parent_id: Optional[int] = Field(default=None, description='菜单父级ID')
    sort: int = Field(default=0, ge=0, description='排序')
    icon: Optional[str] = None
    path: Optional[str] = None
    menu_type: MenuType = Field(default=MenuType.directory, description='菜单类型（0目录 1菜单 2按钮）')
    component: Optional[str] = None
    perms: Optional[str] = None
    status: StatusType = Field(default=StatusType.enable)
    show: StatusType = Field(default=StatusType.enable)
    cache: StatusType = Field(default=StatusType.enable)
    remark: Optional[str] = None

class CreateMenuParam(MenuSchemaBase):
    pass


class UpdateMenuParam(MenuSchemaBase):
    pass


class GetMenuListDetails(MenuSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
    update_time: Optional[datetime] = None
