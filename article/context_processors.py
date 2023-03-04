# -*- coding:utf-8 -*-
"""
作者：71041
日期：2023年03月03日
"""
from .models import ArticleColumn
from .models import ArticlePost


def navigation_bar(request):
    columns = ArticleColumn.objects.all()
    column_number = []
    for item in columns:
        number = ArticlePost.objects.filter(column=item.id).count()
        column_number.append(number)

    columns = zip(columns, column_number)
    contexts = {
        "columnsToAll": columns,
    }
    return contexts
