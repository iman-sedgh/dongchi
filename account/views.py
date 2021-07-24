from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financialmanager.models import deposit
from .forms import AvatarForm, RegisterForm
# Create your views here.


@login_required
def profile_view(request):
    if request.method == 'GET':
        form = AvatarForm()
        data = {'deposits': deposit.objects.all(), 'form': form}
        return render(request, 'account/profile.html', context=data)

    else:  # POST
        user = request.user
        data = request.POST
        avatar_form = AvatarForm(request.POST, request.FILES)
        if avatar_form.is_valid():
            usr = request.user
            usr.avatar = request.FILES['avatar']
            usr.save()
            messages.add_message(request, messages.SUCCESS,
                                 'عکس آواتار شما با موفقیت اصلاح شد')
            return redirect('account:profile')
        elif 'first_name' in data:  # Its  From User details Form
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            #user.phone_number = data['phone']
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'مشخصات شما با موفقیت اصلاح شد')
            return redirect('account:profile')
        elif 'password' in data:  # Its  From password resset Form
            if data['password'] != data['password2']:
                messages.add_message(
                    request, messages.WARNING, 'مقادیر وارد شده برابر نمی باشند')
            else:
                user.set_password(data['password'])
                user.save()
                messages.add_message(
                    request, messages.SUCCESS, 'رمز عبور شما با موفقیت تغییر یافت')
            return redirect('account:profile')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("financialmanager:box_select")
    if request.method == 'GET':
        return render(request, 'account/login.html')
    else:
        data = request.POST
        Username = data['username']
        Password = data['password']
        u = authenticate(username=Username, password=Password)
        if u is not None:
            login(request, u)
            messages.add_message(request, messages.SUCCESS,
                                 'شما با موفقیت وارد شدید')
        else:
            messages.add_message(request, messages.WARNING,
                                 'نام کاربری یا رمز ورود اشتباه است')
        return redirect('financialmanager:box_select')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('financialmanager:home')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('financialmanager:box_select')
        else:
            messages.add_message(request,messages.ERROR,'مقادیر وارد شده را مجددا بررسی کنید')
            return render(request, 'account/register.html', context={'form': form})
    else:
        form = RegisterForm()
        return render(request, 'account/register.html', context={'form': form})
