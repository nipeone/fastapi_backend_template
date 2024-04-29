#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/04/15 14:59:28
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from fastapi import APIRouter

from .auth import router as auth_router
from .captcha import router as captcha_router

router = APIRouter(prefix='/auth', tags=['授权管理'])

router.include_router(auth_router)
router.include_router(captcha_router)