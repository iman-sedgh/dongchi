from django.http.response import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Case, When
from .models import withdraw, safebox, deposit, balance
from account.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


def home_view(request):
    return render(request, 'financialmanager/home.html')


@login_required
def box_view(request, boxslug=''):
    if boxslug == '':
        if request.user.safebox.all():
            slg = request.user.safebox.first().slug
            return redirect('financialmanager:box', boxslug=slg)
        else:
            return render(request, 'financialmanager/box_select.html', context={'nobox': True})

    box = get_object_or_404(safebox, slug=boxslug)
    if not request.user in box.members.all():
        return HttpResponseForbidden()
    else:
        data = {
            "members": User.objects.filter(is_financialstaff=True, safebox=box).order_by(Case(When(id=request.user.id, then=0), default=1), 'id'),
            "boxes": safebox.objects.all(),
            "box": box,
            "box_withdraws": withdraw.objects.filter(box=box),
            "box_deposits": deposit.objects.filter(box=box),
            "balance": balance.objects.all(),
        }
        return render(request, 'financialmanager/box.html', context=data)


def withdraw_view(request):
    if request.method == 'GET':
        data = {
            "boxes": safebox.objects.all(),
            "users": User.objects.all()
        }
        return render(request, 'financialmanager/withdraw.html', context=data)
    if request.method == 'POST':
        data = request.POST
        a = int(data['amount']) / len(data.getlist('payers'))
        payers = []
        for i in data.getlist('payers'):
            payers.append(User.objects.get(id=int(i)))
        model = withdraw(
            amount=data['amount'],
            details=data['description'],
            box=safebox.objects.get(id=data['box'])
        )
        model.save()
        model.payer.set(payers)
        model.save()
        messages.add_message(request, messages.SUCCESS, 'برداشت وجه ثبت شد')
        return redirect("financialmanager:box", boxslug=model.box.slug)


@api_view(['POST'])
def deposit_view(request):  # webhook From IDpay
    data = request.data
    usr = User.objects.get(username=data["payer"]["name"])
    # Safe Box ID is last 'word' in description
    safe_id = data["payer"]["desc"].split()[-1]
    model = deposit(
        user=usr,
        amount=int(data['amount'])/10, #Convert Rial to Toman
        details=' '.join(data["payer"]["desc"].split()[:-1]),
        box=safebox.objects.get(id=safe_id)
    )
    model.save()
    return JsonResponse({'Status': 'Done'})


@api_view(['POST'])
def box_settings(request):
    data = request.POST
    gateway_url = data['gateway_url']
    gateway_type = data['gateway_type']
    box = get_object_or_404(safebox, slug=data['safebox'])
    box.payment_gateway = gateway_url
    box.save()
    messages.add_message(request, messages.SUCCESS,
                         'تنظیمات با موفقیت اعمال شد ')
    return redirect('financialmanager:box', boxslug=box.slug)


@api_view(['POST'])
def box_creation(request):
    data = request.POST
    box = safebox(
        name=data['boxname'],
        creator=request.user,
        details=data['boxdetails'],
        payment_gateway=data['gateway_url'],
        slug=data['boxslug']
    )
    box.save()
    box.members.add(request.user)
    box.save()
    messages.add_message(request, messages.SUCCESS,
                         'صندوق شما با موفقیت ساخته شد')
    return redirect('financialmanager:box_select')


@login_required
def box_join(request, inviteid):
    try:
        box = safebox.objects.get(invite_id=inviteid)
    except:
        messages.add_message(request, messages.ERROR,
                             'لینک دعوت معتبر نمی باشد')
        return redirect('financialmanager:box_select')
    if request.user in box.members.all():
        messages.add_message(request, messages.INFO,
                             'شما در حال حاضر عضو صندوق می باشید')
    else:
        box.members.add(request.user)
        box.save()
        messages.add_message(request, messages.SUCCESS,
                             f' شما با موفقیت به صندوق {box.name} اضافه شدید ')
    return redirect('financialmanager:box_select')
