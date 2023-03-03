# -*- coding:utf-8 -*-
"""
作者：71041
日期：2023年03月03日
"""
from .models import ArticleColumn


def navigation_bar(request):
    contexts = {}
    columns = ArticleColumn.objects.all()
    contexts["columns"] = columns

    return contexts

