from financialmanager.models import deposit
from django import template
from . import jalali
register = template.Library()


def count(deposits, user):
    counter = deposits.filter(user=user)
    return len(counter)


def to_jalali(time):
    date = jalali.Gregorian(time).persian_string().replace('-',',')
    return date


def log_maker(deposits, withdraws):
    logs = []
    logs = list(deposits.all()) + list(withdraws.all())
    logs.sort(key= lambda r : r.date , reverse=True)
    return logs

def get_name(object):
    dictionary = {
        "deposit": "واریزی به صندوق",
        "withdraw": "برداشت از صندوق"
    }
    return dictionary.get(object.__class__.__name__)


register.filter('count', count)
register.filter('to_jalali', to_jalali)
register.filter('log_maker', log_maker)
register.filter('get_name', get_name)
