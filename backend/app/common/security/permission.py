#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   permission.py
@Time    :   2024/04/19 09:36:41
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from fastapi import Request

from backend.app.core.conf import settings
from backend.app.common.exception.errors import ServerError



class RequestPermission:
    """
    请求权限，仅用于角色菜单RBAC

    Tip:
        使用此请求权限时，需要将 `Depends(RequestPermission('xxx'))` 在 `DependsRBAC` 之前设置，
        因为 fastapi 当前版本的接口依赖注入按正序执行，意味着 RBAC 标识会在验证前被设置
    """

    def __init__(self, value: str):
        self.value = value

    async def __call__(self, request: Request):
        if settings.PERMISSION_MODE == 'role-menu':
            if not isinstance(self.value, str):
                raise ServerError
            # 附加权限标识
            request.state.permission = self.value
