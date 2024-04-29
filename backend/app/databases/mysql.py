#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   mysql.py
@Time    :   2024/04/13 18:29:45
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Iterator, TypeVar, AsyncGenerator
import sys
from fastapi import Depends
from typing_extensions import Annotated
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from backend.app.core.conf import settings
from backend.app.common.log import log
from backend.app.models.base import MappedBase

T = TypeVar('T', str, bytes)

DB_SCHEMAS = ["mysql+pymysql", "mysql+asyncmy"]
TEMPLATE = (
    f'{{DB_SCHEMA}}://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
    f'{settings.MYSQL_PORT}/{settings.MYSQL_DB}?charset={settings.MYSQL_CHARSET}'
)

def get_db_url(is_async: bool=True):
    return TEMPLATE.format(DB_SCHEMA=DB_SCHEMAS[is_async])

def create_engine_and_session(url, is_async: bool=True):
    try:
        engine = create_async_engine(url, echo=settings.MYSQL_ECHO, future=True, pool_pre_ping=True) \
                    if is_async else \
                    create_engine(url, echo=settings.MYSQL_ECHO, pool_pre_ping=True)
        
    except Exception as e:
        log.error('❌ 数据库链接失败 {}', e)
        sys.exit()
    else:
        if is_async:
            session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        else:
            session = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, autocommit=False))
        return engine, session

async_engine, async_session = create_engine_and_session(get_db_url())

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()

# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]

async def create_table():
    """创建数据库表"""
    async with async_engine.begin() as con:
        await con.run_sync(MappedBase.metadata.create_all)