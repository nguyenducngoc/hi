# Django imports.
from doctest import master
import email
import mailbox
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.core.mail import EmailMessage
# Blog app imports.
from blog.token import account_activation_token
from blog.forms.account.register_forms import UserRegisterForm


#mail
from django.core.mail import send_mail
from django.conf import settings

import threading


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'account/register.html'
    context_object = {
                       "register_form": UserRegisterForm()
                      }

    def get(self, request):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = True
            user.save()

            current_site = get_current_site(request)
            subject = 'Kích hoạt tài khoản Shuyi Bolg của bạn'
            message = render_to_string('account/account_activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #email_mess = EmailMessage(
            #   subject,
            #    message,
            #    'nguyenducngoc167@gmail.com',
            #    to=[email],
            #)
            recipient_list = [user.email,]
            send_mail(subject,message,'walapa001@gmail.com',recipient_list)
           # email_mess.send()
           # EmailThread(email_mess).start()
            
            return redirect('blog:account_activation_sent')

        else:
            messages.error(request, "Vui lòng cung cấp thông tin hợp lệ.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)


class AccountActivationSentView(View):

    def get(self, request):

        return render(request, 'account/account_activation_sent.html')


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()

            login(request, user)

            username = user.username

            messages.success(request, f"Congratulations {username} !!! "
                                      f"Your account was created and activated "
                                      f"successfully"
                             )

            return redirect('blog:login')
        else:
            return render(request, 'account/account_activation_invalid.html')
