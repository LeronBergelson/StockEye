"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User, Group

class StockList(models.Model):
    stocks = models.CharField(max_length=60, blank=True, default = '')

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    stockResults = models.ManyToManyField('app.StockList')
    