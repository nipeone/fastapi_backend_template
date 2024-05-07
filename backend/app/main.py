#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/04/14 12:39:25
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from backend.app.core.registrar import register_app

"""
pip install uvicorn
# 推荐启动方式 main指当前文件名字 app指FastAPI实例化后对象名称
uvicorn backend.app.main:app --host=127.0.0.1 --port=8000 --reload

类似flask 工厂模式创建
# 生产启动命令 去掉热重载 (可用supervisor托管后台运行)

在main.py同文件下下启动
uvicorn backend.app.main:app --host=127.0.0.1 --port=8000 --workers=4

# 同样可以也可以配合gunicorn多进程启动  main.py同文件下下启动 默认127.0.0.1:8000端口
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000

"""

app = register_app()
