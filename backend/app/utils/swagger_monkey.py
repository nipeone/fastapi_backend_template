#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   swagger.py
@Time    :   2023/12/25 16:20:49
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger-ui.css',
        swagger_favicon_url='/static/favicon.png'
    )
def redoc_monkey_patch(*args, **kwargs):
    return get_redoc_html(
        *args, **kwargs,
        redoc_js_url='/static/redoc.standalone.js',
        redoc_favicon_url='/static/favicon.png'
    )