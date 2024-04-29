#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   router.py
@Time    :   2024/04/14 09:52:54
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from fastapi import APIRouter

from backend.app.core.conf import settings
from .v1.auth import router as auth_router
from .v1.sys import router as sys_router

v1 = APIRouter(prefix=settings.API_V1_STR)
v1.include_router(auth_router)
v1.include_router(sys_router)