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

from .casbin import router as casbin_router
from .dept import router as dept_router
from .dict_data import router as dict_data_router
from .dict_type import router as dict_type_router
from .menu import router as menu_router
from .role import router as role_router
from .user import router as user_router

router = APIRouter()

router.include_router(casbin_router, prefix='/casbin', tags=['Casbin权限管理'])
router.include_router(dept_router, prefix='/depts', tags=['部门管理'])
router.include_router(dict_data_router, prefix='/dict_datas', tags=['字典数据管理'])
router.include_router(dict_type_router, prefix='/dict_types', tags=['字典类型管理'])
router.include_router(menu_router, prefix='/menus', tags=['菜单管理'])
router.include_router(role_router, prefix='/roles', tags=['角色管理'])
router.include_router(user_router, prefix='/users', tags=['用户管理'])

