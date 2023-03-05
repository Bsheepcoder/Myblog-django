# -*- coding:utf-8 -*-
"""
作者：71041
日期：2023年03月02日
"""
# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from userprofile.utils.encrypt import md5


class Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


# 登录表单，继承了 forms.Form 类
class UserLoginForm(Bootstrap, forms.Form):
    username = forms.CharField(label="用户名",
                               widget=forms.TextInput(),
                               required=True,
                               )
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(render_value=True),
                               required=True,
                               )
    code = forms.CharField(label="验证码",
                           widget=forms.TextInput(),
                           required=True,
                           )

    # def clean_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     return md5(pwd)


# 注册用户表单
class UserRegisterForm(Bootstrap, forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField(label="密码")
    password2 = forms.CharField(label="确认密码")

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")
