#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   pagination.py
@Time    :   2024/04/14 10:22:09
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from __future__ import annotations

import math
from typing import TypeVar, Generic, Sequence, Dict, TYPE_CHECKING, Union, Optional, Any
from fastapi import Query, Depends
from fastapi_pagination import pagination_ctx
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links.bases import create_links
from pydantic import BaseModel

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
DataT = TypeVar('DataT')
SchemaT = TypeVar('SchemaT')


class _Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description='Page number')
    size: int = Query(20, gt=0, le=100, description='Page size')  # 默认 20 条记录
    # skip: int = Query(1, ge=1, description='Page number')
    # limit: int = Query(20, gt=0, le=100, description='Page size')  # 默认 20 条记录

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class _Page(AbstractPage[T], Generic[T]):
    items: Sequence[T]  # 数据
    total: int  # 总数据数
    page: int  # 第n页
    size: int  # 每页数量
    total_pages: int  # 总页数
    links: Dict[str, Optional[str]]  # 跳转链接

    __params_type__ = _Params  # 使用自定义的Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: _Params,
    ) -> _Page[T]:
        page = params.page
        size = params.size
        total_pages = math.ceil(total / params.size)
        links = create_links(
            **{
                'first': {'page': 1, 'size': f'{size}'},
                'last': {'page': f'{math.ceil(total / params.size)}', 'size': f'{size}'} if total > 0 else None,
                'next': {'page': f'{page + 1}', 'size': f'{size}'} if (page + 1) <= total_pages else None,
                'prev': {'page': f'{page - 1}', 'size': f'{size}'} if (page - 1) >= 1 else None,
            }
        ).model_dump()

        return cls(items=items, total=total, page=params.page, size=params.size, total_pages=total_pages, links=links)


class _PageData(BaseModel, Generic[DataT]):
    page_data: Optional[DataT] = None


async def paging_data(db: AsyncSession, select: Select, page_data_schema: SchemaT) -> dict:
    """
    基于 SQLAlchemy 创建分页数据

    :param db:
    :param select:
    :param page_data_schema:
    :return:
    """
    _paginate = await paginate(db, select)
    page_data = _PageData[_Page[page_data_schema]](page_data=_paginate).model_dump()['page_data']
    return page_data


# 分页依赖注入
DependsPagination = Depends(pagination_ctx(_Page))