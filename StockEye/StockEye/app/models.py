"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    stockResults = models.ManyToManyField('app.StockList')
    #stockResults = models.ForeignKey('app.StockList', blank=True, default = '', on_delete=models.PROTECT)
    watchList_id = models.PositiveIntegerField(blank=False, default=0)
    watchList_name = models.CharField(max_length=15, blank=False, default = '')

    class Meta:
        get_latest_by = "watchList_id"



class StockList(models.Model):
    stock_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    symbol = models.CharField(max_length=6, blank=False, default = '')
    positiveSentimentCount = models.PositiveIntegerField(blank=False, default=0)
    negativeSentimentCount = models.PositiveIntegerField(blank=False, default=0)
    value = models.FloatField(blank=False, default = 0.0)
    tweet_id = models.CharField(max_length=6, blank=True, default = '')

    def __str__(self):
        return self.symbol

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    watchList = models.ManyToManyField('app.WatchList')

    class Meta:
        ordering = ['user']
    