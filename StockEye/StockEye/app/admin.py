from django.contrib import admin
from app.models import UserData, StockList, WatchList

admin.site.register(UserData)
admin.site.register(StockList)
admin.site.register(WatchList)