from django.contrib import admin
from .models import Vendors,PurchaseOrder,HistoricalPerformanceModel
# Register your models here.
admin.site.register(Vendors)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformanceModel)