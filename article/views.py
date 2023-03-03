import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
# Create your views here.
# 导入数据模型ArticlePost
from .models import ArticlePost, ArticleColumn
# 引入HttpResponse
from django.http import HttpResponse, JsonResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入 Q 对象
from django.db.models import Q
from .models import ArticleColumn

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if column:
            column_id = ArticleColumn.objects.filter(title=column).first().id
            if order == 'total_views':
                article_list = ArticlePost.objects.filter(column=column_id).order_by('-total_views')
            else:
                article_list = ArticlePost.objects.filter(column=column_id)
        else:
            if order == 'total_views':
                article_list = ArticlePost.objects.all().order_by('-total_views')
            else:
                article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')

    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


# 找到markdown中的frontmatter属性
def find(str):
    # 返回字典
    result = {}
    # 记录识别---
    tag = 0
    # 格式化str
    strArray = str.split()
    # 记录frontmatter的字符数
    count = 0
    for i, v in enumerate(strArray):
        if v == '---':
            count += 9
            tag += 1
        if tag == 1:
            istitle = strArray[i + 1]
            isinfo = strArray[i + 2]
            if istitle[-1] == ':' and istitle != '---':
                count = count + len(istitle) + 1
                if isinfo[-1] != ':' and istitle != '---':
                    count = count + len(isinfo)
                    result[istitle[0:-1]] = isinfo
    return result, count


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    body = article.body

    # 浏览量 +1,没有对不同ip设置
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 查看md中是否有frontmatter
    frontmatter, num = find(body[0:100])
    if frontmatter != {}:
        article.title = frontmatter['title']
    # 需要传递给模板的对象
    context = {'article': article,
               'body': json.dumps(body[num:-1]), }

    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form,
                   'columns': columns,
                   }
        return render(request, 'article/create.html', context)


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")

        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 提醒用户登录
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 新增的代码
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns, }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


def article_column(request):
    columnlist = ArticleColumn.objects.all()

    return render(request, {'columnlist': columnlist})
