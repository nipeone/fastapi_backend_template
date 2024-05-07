#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   init_db.py
@Time    :   2024/04/13 20:16:21
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
import asyncio

from backend.app.common.log import log
from backend.app.crud.crud_user import user_dao
from backend.app.schemas.user import RegisterSuperUserParam
from backend.app.core.conf import settings
from backend.app.databases import async_session

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

async def initialize_superuser() -> None:
    '''
        Tables should be created with Alembic migrations
        But if you don't want to use migrations, create
        the tables un-commenting the next line
        Base.metadata.create_all(bind=engine)
    '''
    async with async_session.begin() as db:
        user = await user_dao.get_by_username(db, username=settings.FIRST_SUPERUSER_NAME)
        if not user:
            user_in = RegisterSuperUserParam(
                username=settings.FIRST_SUPERUSER_NAME,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                nickname=settings.FIRST_SUPERUSER_NAME,
                email=settings.FIRST_SUPERUSER_EMAIL,
                is_superuser=True
            )
            user = await user_dao.register(db, obj=user_in)  # noqa: F841
            log.info(f"create root user successfully")
        else:
            log.info(f"root user has exists")

async def main() -> None:
    log.info("Creating initial data")
    await initialize_superuser()
    log.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())