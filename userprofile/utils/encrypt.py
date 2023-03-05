# -*- coding:utf-8 -*-
"""
作者：71041
日期：2023年03月05日
"""
from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
