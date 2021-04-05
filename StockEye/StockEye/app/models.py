"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User, Group
#from django.contrib.postgres.fields import ArrayField

#class StockList(models.Model):
#    stocksArray = ArrayField(
#        ArrayField(
#            models.CharField(max_length=10, blank=True),
#            size=8,
#        ),
#        size=8,
#    )

class UserData(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
 #   stockresults = models.ManyToManyField('app.StockList', )