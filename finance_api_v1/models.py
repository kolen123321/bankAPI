from django.db import models

from accounts.models import User

from .managers import FinanceProfileManager

class FinanceProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    freezed = models.BooleanField(default=False)
    objects = FinanceProfileManager()
    title = models.CharField(max_length=32, default='')

class Transaction(models.Model):

    from_profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE, related_name='from_profile', null=True, blank=True)
    to_profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE, related_name='to_profile', null=True, blank=True)
    amount = models.FloatField(null=False)
    status = models.CharField(default='success', max_length=16)


# Не реализовано

class Request(models.Model):

    requester = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE, related_name='requester')
    payer = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE, related_name='payer')
    amount = models.FloatField(null=False)
    message = models.TextField()
    status = models.CharField(default='waiting', max_length=16)