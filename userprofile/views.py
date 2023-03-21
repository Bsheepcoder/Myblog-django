from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
# 引入 UserRegisterForm 表单类
from .forms import UserLoginForm, UserRegisterForm
from .utils.imgCode import check_code


# Create your views here.

def user_login(request):
    user_login_form = UserLoginForm(data=request.POST)
    if request.method == 'GET':
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)

    if user_login_form.is_valid():
        user_input_code = user_login_form.cleaned_data.pop('code')
        session_code = request.session.get('image_code')

        if user_input_code == session_code:
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user:
                request.session.set_expiry(60 * 60 * 24 * 7)  # 60s超时
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("article:article_list")
            user_login_form.add_error("password", "用户名或密码错误")
            context = {'form': user_login_form}
            return render(request, 'userprofile/login.html', context)

        user_login_form.add_error("code", "验证码错误")
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    context = {'form': user_login_form}
    return render(request, 'userprofile/login.html', context)


from io import BytesIO


# 验证码
def imge_code(request):
    img, check_char = check_code()

    # 写入session
    request.session['image_code'] = check_char
    request.session.set_expiry(60)  # 60s超时

    # 在内存中创建文件
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
