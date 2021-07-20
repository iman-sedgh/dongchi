from django.db import models
from account.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


# Create your models here.


class safebox(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=1000, blank=True)
    balance = models.BigIntegerField()


class deposit(models.Model):  # put money
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=1000, blank=True)
    box = ForeignKey(safebox, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        self.box.balance += self.amount
        self.box.save()
        self.user.balance += self.amount
        self.user.save()
        super(deposit, self).save(*args, **kwargs)


class withdraw(models.Model):  # take money

    payer = models.ManyToManyField(User, default=User.objects.all)
    amount = models.BigIntegerField()
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=1000, blank=True)
    box = ForeignKey(safebox, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        super(withdraw, self).save(*args, **kwargs)
        if(len(self.payer.all()) ==0 ):
            return 
        a = int(self.amount) / len(self.payer.all())
        for payer in self.payer.all():
            payer.balance -= a
            payer.save()
        self.box.balance -= int(self.amount)
        self.box.save()
        super(withdraw, self).save(*args, **kwargs)





#        for user in self.payer:
#            user.balance -= self.amount / payers
#            user.save()
