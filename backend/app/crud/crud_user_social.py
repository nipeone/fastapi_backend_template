#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   crud_user_social.py
@Time    :   2024/04/19 09:19:28
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.enums import UserSocialType
from backend.app.models import UserSocial
from backend.app.schemas.user_social import CreateUserSocialParam, UpdateUserSocialParam
from backend.app.crud.crud_base import CRUDBase


class CRUDOUserSocial(CRUDBase[UserSocial, CreateUserSocialParam, UpdateUserSocialParam]):

    async def get_by_socialtype(self, db: AsyncSession, user_id: int, source: UserSocialType) -> UserSocial | None:
        """
        获取用户社交账号绑定

        :param db:
        :param user_id:
        :param source:
        :return:
        """
        se = select(self.model).where(and_(self.model.user_id == user_id, self.model.source == source))
        user_social = await db.execute(se)
        return user_social.scalars().first()
    
user_social_dao: CRUDOUserSocial = CRUDOUserSocial(UserSocial)