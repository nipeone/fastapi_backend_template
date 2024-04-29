#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   fastapp.py
@Time    :   2024/04/13 15:42:06
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
import os
from contextlib import asynccontextmanager
from pydantic import ValidationError
from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware

from backend.app.utils.swagger_monkey import swagger_monkey_patch, redoc_monkey_patch
from backend.app.api.router import v1 as v1_router
from backend.app.common.exception.exception_handler import register_exception
from backend.app.core.conf import settings
from backend.app.core.path_conf import STATIC_DIR, UPLOAD_DIR
from backend.app.common.log import log
from backend.app.common.cache.redis import redis_client
from backend.app.databases.mysql import create_table
from backend.app.middlewares.jwt_auth_middleware import JwtAuthMiddleware
from backend.app.middlewares.opera_log_middleware import OperaLogMiddleware
from backend.app.utils.health_check import ensure_unique_route_names, http_limit_callback
from backend.app.utils.openapi import simplify_operation_ids
from backend.app.init_superuser import initialize_superuser
from backend.app.utils.serializers import MsgSpecJSONResponse

@asynccontextmanager
async def register_init(app: FastAPI):
    """
    初始化连接
    :param app:
    :return:
    """
    from fastapi import applications
    applications.get_swagger_ui_html = swagger_monkey_patch
    applications.get_redoc_html = redoc_monkey_patch

    # 打印配置
    print_settings()

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    await create_table()

    await initialize_superuser()

    # 启动 redis
    await redis_client.startup()

    # 初始化 limiter
    await FastAPILimiter.init(redis_client, prefix=settings.LIMITER_REDIS_PREFIX, http_callback=http_limit_callback)
    
    yield

    # 关闭 redis
    await redis_client.shutdown()

    # 关闭 limiter
    await FastAPILimiter.close()

def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESC,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
    )

    # 静态文件
    register_static_file(app)

    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 分页
    register_page(app)

    # 全局异常处理
    register_exception(app)

    return app

def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式使用，生产使用 nginx 静态资源服务，这里是开发是方便本地
    :param app:
    :return:
    """
    if settings.STATIC_FILES:
        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

def register_middleware(app: FastAPI):
    """
    中间件，执行顺序从下往上

    :param app:
    :return:
    """
    # Gzip: Always at the top
    if settings.MIDDLEWARE_GZIP:
        from fastapi.middleware.gzip import GZipMiddleware

        app.add_middleware(GZipMiddleware)
    # Opera log
    app.add_middleware(OperaLogMiddleware)
    # JWT auth, required
    app.add_middleware(
        AuthenticationMiddleware, backend=JwtAuthMiddleware(), on_error=JwtAuthMiddleware.auth_exception_handler
    )
    # Access log
    if settings.MIDDLEWARE_ACCESS:
        from backend.app.middlewares.access_middleware import AccessMiddleware

        app.add_middleware(AccessMiddleware)
    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

def register_router(app: FastAPI):
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(v1_router)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)

def register_page(app: FastAPI):
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)

def print_settings():
    try:
        log.info("pcloud is starting with config:")
        for k, v in settings.model_dump().items():
            log.info(f"{k}: {v}")
    except ValidationError as e:
        log.error("Impossible to read or parse some settings:")
        log.error(e)
        exit(-1)