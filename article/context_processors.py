# -*- coding:utf-8 -*-
"""
作者：71041
日期：2023年03月03日
"""
from .models import ArticleColumn
from .models import ArticlePost
import time
from django.conf import settings
from django.db.models import Sum

def columns_tag(request):
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


def article_count(request):
    # 文章总数统计
    num = ArticlePost.objects.all().count()
    # 文章总浏览量统计
    article_view = ArticlePost.objects.all().aggregate(Sum('total_views'))
    contexts = {
        "article_number": num,
        "article_views": article_view['total_views__sum'],
    }
    return contexts


def runtime_now(request):
    nowTime = time.time()
    beginTime = int(time.mktime(time.strptime(settings.BEGIN_TIME, "%Y-%m-%d")))
    runTime = nowTime - beginTime
    days = int(runTime / (60 * 60 * 24))
    contexts = {
        "runtime_days": days,
    }
    return contexts
