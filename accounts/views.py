from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
#import ghasedak
from django.core.mail.message import EmailMessage




def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'], email=data['email_address'],
                                     password=data['password2'])
            messages.success(request, 'خوش آمدید ثبت نام با موفقیت انجام شد', 'primary')
            user.is_active = False
            user.save()
            email = EmailMessage{
                'active user',
                'hello user',
                'test<>',
                [data['email_address']]
            }
            email.send(fail_silently=False)
            return redirect('home:home')
    else:
        form = UserRegisterForm()
        context = {'form': form}
    return render(request, 'accounts/register.html', {'form': form})
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
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
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