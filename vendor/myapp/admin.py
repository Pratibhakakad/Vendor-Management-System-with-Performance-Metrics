from django.contrib import admin
from .models import VendorModel,PuchaseorderModel, HistoricalPerformance

# Register your models here.
admin.site.register(VendorModel)
admin.site.register(PuchaseorderModel)
admin.site.register( HistoricalPerformance)
