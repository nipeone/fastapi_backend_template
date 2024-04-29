#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   path_conf.py
@Time    :   2024/04/13 15:02:07
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALEMBIC_VER_DIR = os.path.join(BASE_DIR, 'app', 'alembic', 'versions')

# 日志文件路径
LOG_DIR = os.path.join(BASE_DIR, 'app', 'log')

ASSETS_DIR = os.path.join(BASE_DIR, 'app', 'assets')

# 静态文件目录
STATIC_DIR = os.path.join(ASSETS_DIR, 'static')

# 文件上传路径
UPLOAD_DIR = os.path.join(ASSETS_DIR, 'upload')

# 离线 IP 数据库路径
IP2REGION_XDB = os.path.join(STATIC_DIR, 'ip2region.xdb')