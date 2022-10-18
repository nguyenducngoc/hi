# Django imports.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

# Blog app imports
from blog.forms.account.login_forms import UserLoginForm


class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'account/login.html'
    context_object = {"login_form": UserLoginForm}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        login_form = UserLoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Đăng nhập thành công!"
                                          f"Chào mừng {user.username}.")
                return redirect('blog:dashboard_home')

            else:
                messages.error(request,
                               f"Thông tin đăng nhập không hợp lệ: {username}, {password} "
                               f"tên người dùng và mật khẩu không hợp lệ !!! Xin vui lòng "
                               f"nhập tên người dùng và mật khẩu lại.")
                return render(request, self.template_name, self.context_object)

        else:
            messages.error(request, f"Tên người dùng và mật khẩu không hợp lệ")
            return render(request, self.template_name, self.context_object)



