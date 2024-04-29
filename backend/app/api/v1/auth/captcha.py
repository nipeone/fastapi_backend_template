#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   captcha.py
@Time    :   2024/04/15 14:56:52
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Annotated
from fast_captcha import img_captcha
from fastapi import APIRouter, Depends, Request, Query
from fastapi_limiter.depends import RateLimiter
from starlette.concurrency import run_in_threadpool

from backend.app.core.conf import settings
from backend.app.common.cache.redis import redis_client
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.common.log import log
from backend.app.utils.request_parse import get_request_ip

router = APIRouter()

@router.get('/captcha', summary='获取登录验证码', dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def get_captcha(
    request: Request,
    width: Annotated[int, Query()] = 120,
    height: Annotated[int, Query()] = 40,
    ):
    """
    此接口可能存在性能损耗，尽管是异步接口，但是验证码生成是IO密集型任务，使用线程池尽量减少性能损耗
    """
    img_type: str = 'base64'
    code_length = 4
    img, code = await run_in_threadpool(img_captcha, width=width, height=height, img_byte=img_type)
    ip = await get_request_ip(request)
    log.debug(code)
    await redis_client.set(
        f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ip}', code, settings.CAPTCHA_LOGIN_EXPIRE_SECONDS
    )
    return await response_base.success(data={'image_type': img_type, 'image': img, 'code_length': code_length})