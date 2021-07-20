from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from financialmanager.models import deposit
from .forms import AvatarForm
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
        return redirect('financialmanager:home')


def logout_view(request):
    pass
