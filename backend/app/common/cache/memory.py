#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   memory.py
@Time    :   2023/10/16 17:09:16
@Author  :   xy 
@Version :   1.0
@Copyright : ©Copyright 2020-2023 Wukong Company
@Desc    :   None
'''
from typing import Any
from collections import OrderedDict
from copy import deepcopy

from backend.app.core.conf import settings


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Any:
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class ImageLRUCache(LRUCache):
    def get(self, key: str) -> Any:
        image = super().get(key)
        if image is None:
            return None
        cloned = deepcopy(image)
        self.cache[key] = cloned
        return cloned


image_cache = ImageLRUCache(settings.MEMORY_LRU_CACHE_CAPACITY)
custom_cache = LRUCache(settings.MEMORY_LRU_CACHE_CAPACITY)