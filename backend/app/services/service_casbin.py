#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   service_casbin.py
@Time    :   2024/04/19 09:32:22
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from uuid import UUID

from backend.app.schemas.casbin_rule import (
    CreatePolicyParam,
    CreateUserRoleParam,
    DeleteAllPoliciesParam,
    DeletePolicyParam,
    DeleteUserRoleParam,
    UpdatePolicyParam,
    GetPolicyListDetails
)
from backend.app.common.pagination import paging_data
from backend.app.common.exception import errors
from backend.app.common.security.rbac import rbac
from backend.app.databases.mysql import async_session
from backend.app.services.service_base import ServiceBase
from backend.app.crud import casbin_dao, CRUDCasbin
from backend.app.models import CasbinRule
from backend.app.schemas.casbin_rule import CreateUserRoleParam, UpdatePolicyParam

class ServiceCasbin(ServiceBase[CasbinRule, CreateUserRoleParam, UpdatePolicyParam]):
    
    def __init__(self, crud_dao: CRUDCasbin):
        super().__init__(crud_dao)
        self.crud_dao: CRUDCasbin

    async def get_pagination(self, *, ptype:str, sub:str):
        select_stmt = self.crud_dao.get_select_list(ptype=ptype, sub=sub)
        async with async_session() as db:
            page_data = await paging_data(db, select_stmt, GetPolicyListDetails)
        return page_data
    
    async def get_policy_list(self, *, role: Optional[int] = None) -> list:
        enforcer = await rbac.enforcer()
        if role is not None:
            data = enforcer.get_filtered_named_policy('p', 0, str(role))
        else:
            data = enforcer.get_policy()
        return data

    async def create_policy(self, *, p: CreatePolicyParam) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data
    
    async def create_policies(self, *, ps: list[CreatePolicyParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data
    
    async def update_policy(self, *, old: UpdatePolicyParam, new: UpdatePolicyParam) -> bool:
        enforcer = await rbac.enforcer()
        _p = enforcer.has_policy(old.sub, old.path, old.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.update_policy([old.sub, old.path, old.method], [new.sub, new.path, new.method])
        return data
    
    async def update_policies(self, *, old: list[UpdatePolicyParam], new: list[UpdatePolicyParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.update_policies(
            [list(o.model_dump().values()) for o in old], [list(n.model_dump().values()) for n in new]
        )
        return data
    
    async def delete_policy(self, *, p: DeletePolicyParam) -> bool:
        enforcer = await rbac.enforcer()
        _p = enforcer.has_policy(p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_policy(p.sub, p.path, p.method)
        return data
    
    async def delete_policies(self, *, ps: list[DeletePolicyParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.remove_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data
    
    async def delete_all_policies(self, *, sub: DeleteAllPoliciesParam) -> int:
        async with async_session.begin() as db:
            count = await self.crud_dao.delete_policies_by_sub(db, sub=sub)
        return count
    
    async def get_group_list(self) -> list:
        enforcer = await rbac.enforcer()
        data = enforcer.get_grouping_policy()
        return data
    
    async def create_group(self, *, g: CreateUserRoleParam) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data
    
    async def create_groups(self, *, gs: list[CreateUserRoleParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data
    
    async def delete_group(self, *, g: DeleteUserRoleParam) -> bool:
        enforcer = await rbac.enforcer()
        _g = enforcer.has_grouping_policy(g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_grouping_policy(g.uuid, g.role)
        return data
    
    async def delete_groups(self, *, gs: list[DeleteUserRoleParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.remove_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data
    
    async def delete_all_groups(self, *, uuid: UUID) -> int:
        async with async_session.begin() as db:
            count = await self.crud_dao.delete_groups_by_uuid(db, uuid=uuid)
        return count
    
casbin_service = ServiceCasbin(casbin_dao)