#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2024/04/13 20:18:24
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from pydantic import BaseModel, ConfigDict, EmailStr, validate_email
from pydantic_extra_types.phone_numbers import PhoneNumber
class CustomPhoneNumber(PhoneNumber):
    default_region_code = 'CN'


class CustomEmailStr(EmailStr):
    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return None if __input_value == '' else validate_email(__input_value)[1]
    
class SchemaBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="ignore")