from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Case, When
from .models import withdraw, safebox, deposit, balance
from account.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@login_required
def home_view(request):
    return render(request, 'financialmanager/home.html')


@login_required
def box_view(request, boxslug=''):
    if boxslug == '':
        slg = request.user.safebox.first().slug
        return redirect('financialmanager:box', boxslug=slg)
    box = get_object_or_404(safebox, slug=boxslug)
    if not request.user in box.members.all():
        raise Http404(request)
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
        return redirect("financialmanager:home")


@api_view(['GET', 'POST'])
def deposit_view(request):
    if request.method == 'GET':
        print(""" hey I'm Here GET """)
        print(request.method)
        return Response({'method': 'GET'})

    elif request.method == 'POST':  # webhook From IDpay
        data = request.data
        model = deposit(
            user=User.objects.get(username=data['name']),
            amount=data['amount'],
            details=data['payer']['desc'],
            box=safebox.objects.get(id=1)
        )
        model.save()

        return Response({'Status': 'Done'})


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
    return redirect('financialmanager:box',boxslug = box.slug)
