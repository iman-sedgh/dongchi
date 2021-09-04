from django.contrib.admin.sites import DefaultAdminSite
from django.db import models
from account.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
import uuid


# Create your models here.


class safebox(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE , related_name='founder',null=True)
    members = models.ManyToManyField(User,related_name='safebox')
    details = models.CharField(max_length=1000, blank=True)
    balance = models.BigIntegerField(default=0)
    payment_gateway = models.URLField(blank=True)
    slug = models.SlugField(unique=True)
    invite_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.name)

class balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    safebox = models.ForeignKey(safebox ,on_delete=models.CASCADE ,related_name='box')
    balance = models.IntegerField(default=0)

class deposit(models.Model):  # put money
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=1000, blank=True)
    box = ForeignKey(safebox, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        usr_balance = balance.objects.get_or_create(user= self.user , safebox = self.box)[0]
        self.box.balance += self.amount
        self.box.save()
        usr_balance.balance += self.amount
        usr_balance.save()
        super(deposit, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.amount) + ' --> ' + str(self.box) 


class withdraw(models.Model):  # take money

    payer = models.ManyToManyField(User)
    amount = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=1000, blank=True)
    box = ForeignKey(safebox, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        super(withdraw, self).save(*args, **kwargs)
        if(len(self.payer.all()) ==0 ):#sends from Admin panel
            return 
        a = int(self.amount) / len(self.payer.all())
        for payer in self.payer.all():
            payer_balance = balance.objects.get_or_create(user = payer , safebox = self.box)[0]
            payer_balance.balance -= a
            payer_balance.save()
        self.box.balance -= int(self.amount)
        self.box.save()
        super(withdraw, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.box) + ' --> ' + str(self.amount) 


#        for user in self.payer:
#            user.balance -= self.amount / payers
#            user.save()
