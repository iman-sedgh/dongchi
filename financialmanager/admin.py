from financialmanager.models import withdraw
from django.contrib import admin
from .models import withdraw, deposit, safebox, balance
from account.models import User
# Register your models here.

# class depositAdmin(admin.ModelAdmin):
#    def save_model(self, request, obj, form, change):
#        self.box.balance += self.amount
#        obj.save(form=form)


class withdrawAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        a = obj.amount / len(form['payer'].value())
        for id in form['payer'].value():
            usr = User.objects.get(id=id)
            usr_balance = balance.objects.get_or_create(user =usr , safebox = obj.box)[0]
            usr_balance.balance -= a
            usr_balance.save()
        obj.box.balance -= obj.amount
        obj.box.save()
        obj.save()
    list_display = ('__str__','amount','date')
    

class safeboxAdmin(admin.ModelAdmin): 
    pass


admin.site.register(withdraw, withdrawAdmin)
admin.site.register(deposit)
admin.site.register(safebox, safeboxAdmin)
