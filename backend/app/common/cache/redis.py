#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   redis.py
@Time    :   2024/04/13 17:05:27
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Optional, Union
import sys
from redis.asyncio.client import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.app.common.log import log
from backend.app.core.conf import settings


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,  # 转码 utf-8
        )

    async def startup(self):
        """
        触发初始化连接

        :return:
        """
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ 数据库 redis 连接超时')
            sys.exit()
        except AuthenticationError:
            log.error('❌ 数据库 redis 连接认证失败')
            sys.exit()
        except Exception as e:
            log.error('❌ 数据库 redis 连接异常 {}', e)
            sys.exit()

    async def shutdown(self):
        await self.close()

    async def delete_prefix(self, prefix: str, exclude: Optional[Union[str, list]] = None):
        """
        删除指定前缀的所有key

        :param prefix:
        :param exclude:
        :return:
        """
        keys = []
        for key in await self.keys(f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        if len(keys) > 0:
            await self.delete(*keys)


# 创建 redis 客户端实例
redis_client = RedisCli()