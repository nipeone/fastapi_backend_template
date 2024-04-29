#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   conf.py
@Time    :   2024/04/13 14:29:29
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import List, Literal, Optional
from functools import lru_cache
from pydantic import model_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.app.core.path_conf import BASE_DIR

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env', env_file_encoding='utf-8', case_sensitive=True, extra='allow')

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    # FastAPI
    APP_NAME: str = "pcloud"
    APP_VERSION: str = "0.0.1"
    APP_DESC: str = "pcloud tool kit"
    API_V1_STR: str = "/api/v1"
    DOCS_URL: str = f'{API_V1_STR}/docs'
    REDOCS_URL: str = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str = f'{API_V1_STR}/openapi'

    @model_validator(mode='before')
    @classmethod
    def validator_api_url(cls, values):
        if values['ENVIRONMENT'] == 'pro':
            values['OPENAPI_URL'] = None
        return values
    
    # System
    FIRST_SUPERUSER_NAME: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "password"
    FIRST_SUPERUSER_EMAIL: str = "x0601y@126.com"

    STATIC_FILES: bool = True
    USERS_OPEN_REGISTRATION: bool = True

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # 算法
    TOKEN_SECRET_KEY: str
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1 # 过期时间，单位：秒
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 刷新过期时间，单位：秒
    TOKEN_URL_SWAGGER: str = f'{API_V1_STR}/auth/swagger_login'
    TOKEN_REDIS_PREFIX: str = f'{APP_NAME}_access_token'
    TOKEN_REFRESH_REDIS_PREFIX: str = f'{APP_NAME}_access_refresh_token'
    TOKEN_EXCLUDE: list[str] = [  # 白名单
        f'{API_V1_STR}/auth/login/swagger',
        f'{API_V1_STR}/auth/login',
    ]

    # Task
    TASK_QUEUE_ENABLED: bool = True
    TASK_QUEUE_USER: str = "admin"
    TASK_QUEUE_PASSWORD: str = "password"
    TASK_QUEUE_HOST: str = "localhost"
    TASK_QUEUE_PORT: int = 5672
    TASK_QUEUE_URL: str = f"{TASK_QUEUE_HOST}:{TASK_QUEUE_PORT}" 

    # Redis
    MEMORY_LRU_CACHE_CAPACITY: int = 500
    CACHE_ENABLED: bool = True
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = "6379"
    REDIS_PASSWORD: str = "password"
    REDIS_DATABASE: int = 0
    REDIS_TIMEOUT: int = 5
    REDIS_URL: str = f"{REDIS_HOST}:{REDIS_PORT}"

    # MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DATABASE: str = f"{APP_NAME}"
    MYSQL_ECHO: bool = False
    MYSQL_CHARSET: str = "utf8mb4"

    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True

    LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'

    # Limiter
    LIMITER_REDIS_PREFIX: str = f'{APP_NAME}_limiter'

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Captcha
    CAPTCHA_LOGIN_REDIS_PREFIX: str = f'{APP_NAME}_login_captcha'
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 15  # 过期时间，单位：秒

    # Log
    LOG_STDOUT_FILENAME: str = f'{APP_NAME}_access.log'
    LOG_STDERR_FILENAME: str = f'{APP_NAME}_error.log'

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = False

    # RBAC Permission
    PERMISSION_MODE: Literal['casbin', 'role-menu'] = 'casbin'
    PERMISSION_REDIS_PREFIX: str = f'{APP_NAME}_permission'

    CASBIN_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{API_V1_STR}/auth/logout'),
        ('POST', f'{API_V1_STR}/auth/token/new')
    }

    # Opera log
    OPERA_LOG_EXCLUDE: list[str] = [
        '/favicon.ico',
        DOCS_URL,
        REDOCS_URL,
        OPENAPI_URL,
        f'{API_V1_STR}/auth/swagger',
        f'{API_V1_STR}/auth/github/callback',
    ]
    OPERA_LOG_ENCRYPT: int = 1  # 0: AES (性能损耗); 1: md5; 2: ItsDangerous; 3: 不加密, others: 替换为 ******
    OPERA_LOG_ENCRYPT_INCLUDE: list[str] = ['password', 'old_password', 'new_password', 'confirm_password']

    # ip location
    IP_LOCATION_REDIS_PREFIX: str = f'{APP_NAME}_ip_location'
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # 过期时间，单位：秒

@lru_cache()
def get_settings():
    return Settings()

settings=get_settings()