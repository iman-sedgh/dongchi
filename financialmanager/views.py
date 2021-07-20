from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import withdraw, safebox, deposit
from account.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@login_required
def home(request):
    data = {
        "users": User.objects.filter(is_financialstaff=True),
        "boxes": safebox.objects.all(),
        "withdraws": withdraw.objects.all(),
        "deposits": deposit.objects.all()
    }
    return render(request, 'financialmanager/home.html', context=data)


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
        messages.add_message(request,messages.SUCCESS,'برداشت وجه ثبت شد')
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

