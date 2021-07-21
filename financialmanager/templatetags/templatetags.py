from financialmanager.models import balance, deposit,withdraw
from django import template
from django.utils import timezone
from . import jalali
register = template.Library()


def count(deposits, user):
    counter = deposits.filter(user=user)
    return len(counter)


def to_jalali(time):
    date = jalali.Gregorian(time.date()).persian_string().replace('-',',')
    return date


def log_maker(box):
    logs = []
    logs = list(deposit.objects.filter(box=box)) + list(withdraw.objects.filter(box=box))
    logs.sort(key= lambda r : r.date ,reverse=True)
    return logs

def get_name(object):
    dictionary = {
        "deposit": "واریزی به صندوق",
        "withdraw": "برداشت از صندوق"
    }
    return dictionary.get(object.__class__.__name__)

def get_balance(box , user):
    return balance.objects.get_or_create(user =user , safebox=box)[0].balance

def get_time(log): 
    time = timezone.localtime(log.date)
    return time.strftime("%I:%M%p")

register.filter('count', count)
register.filter('to_jalali', to_jalali)
register.filter('log_maker', log_maker)
register.filter('get_name', get_name)
register.filter('get_balance', get_balance)
register.filter('get_time', get_time)
