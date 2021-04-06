"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User, Group

class StockList(models.Model):
    stocks = models.CharField(max_length=60, blank=True, default = '')
    postiveSentimentCount = models.PositiveIntegerField(default=0)
    negativeSentimentCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.stocks

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    stockResults = models.ManyToManyField('app.StockList')

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f'{self.user}\n{self.stockResults}'
    