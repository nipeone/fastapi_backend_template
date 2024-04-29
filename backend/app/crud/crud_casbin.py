#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_casbin.py
@Time    :   2024/04/18 09:00:20
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from uuid import UUID

from sqlalchemy import Select, and_, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_base import CRUDBase
from backend.app.models import CasbinRule
from backend.app.schemas.casbin_rule import CreatePolicyParam, DeleteAllPoliciesParam, UpdatePolicyParam



class CRUDCasbin(CRUDBase[CasbinRule, CreatePolicyParam, UpdatePolicyParam]):

    def get_select_list(self, ptype: str, sub: str) -> Select:
        """
        获取策略列表

        :param ptype:
        :param sub:
        :return:
        """
        se = select(self.model).order_by(self.model.id)
        where_list = []
        if ptype:
            where_list.append(self.model.ptype == ptype)
        if sub:
            where_list.append(self.model.v0.like(f'%{sub}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def delete_policies_by_sub(self, db: AsyncSession, sub: DeleteAllPoliciesParam) -> int:
        """
        删除角色所有P策略

        :param db:
        :param sub:
        :return:
        """
        where_list = []
        if sub.uuid:
            where_list.append(self.model.v0 == sub.uuid)
        where_list.append(self.model.v0 == sub.role)
        result = await db.execute(delete(self.model).where(or_(*where_list)))
        return result.rowcount
    
    async def delete_groups_by_uuid(self, db: AsyncSession, uuid: UUID) -> int:
        """
        删除用户所有G策略

        :param db:
        :param uuid:
        :return:
        """
        result = await db.execute(delete(self.model).where(self.model.v0 == str(uuid)))
        return result.rowcount
    
casbin_dao: CRUDCasbin = CRUDCasbin(CasbinRule)