from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render, redirect
from .forms import *
from order.models import ItemOrder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
#import ghasedak
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse

class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int):
        return (text_type(user.is_active)+text_type(user.id)+text_type(user.timestamp))
    
email_generator = EmailToken()

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'], email=data['email_address'],
                                     password=data['password2'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active', kwarg={'uidb64':uidb64, 'token':email_generator.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage[
                'active user',
                link,
                'test<>',
                [data['email_address']]
            ]
            email.send(fail_silently=False)
            messages.success(request, 'کاربر محترم جهت فعال سازی به ایمیل خود  مراجعه کنید', 'primary')
            return redirect('home:home')
    else:
        form = UserRegisterForm()
        context = {'form': form}
    return render(request, 'accounts/register.html', {'form': form})

class RegisterEmail(View):
    def get(request, uidb64, token):
        id = (force_text(urlsafe_base64_decode(uidb64)))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')
    
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                username = authenticate(request, username=User.objects.get(email=data['username'])
                                        , password=data['password'])
            except:
                username = authenticate(request, username=data['username'], password=data['password'])
            if username is not None:
                login(request, username)
                messages.success(request, 'با موفقیت وارد شدید', 'primary')
                return redirect('home:home')
            else:
                messages.error(request, 'username or password is wrong', 'danger')


    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید', 'warning')
    return redirect('home:home')

@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(User=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'update successfully', 'success')
            return redirect('accounts:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/update.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'رمز عبور با موفقیت تغییر یافت','success')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'تغییر رمز ناموفق', 'warning')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change.html',{'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneForms(request.POST)
        if form.is_valid():
            data = form.changed_data
            global random_code, phone
            phone_number = f"0{data['phone']}"
            random_code = randint(1000, 10000)
            # gasedak code
            # gasedak code
            return redirect('accounts:verify')

    else:
        form = PhoneForms()
    return render(request, 'accounts/phone.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            data = form.changed_data
            if random_code == data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                messages.success(request, 'Hi user', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'ورود ناموفق', 'warning')

    else:
        form = CodeForm(request.user)
    return render(request, 'accounts/verify.html', {'form': form})

def favorite(request):
    product = request.user.fa_user.all()    
    return render(request, 'accounts/favorite.html' {'product':product})

def history(request):
    data = ItemOrder.objects.filter(user_id=request.user.id)
    return render( request,'account/history.html'{'data':data } )
 
class ResetPassword(auth_views.PasswordResetView):
    template_name ='accounts:reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'acconts:link.html'
    
class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts:done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts:complete.html'


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts:complete.html'


