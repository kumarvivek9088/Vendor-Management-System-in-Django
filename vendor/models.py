from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .utils import calculate_on_time_delivery_rate,calculate_quality_rating_average,calculate_avg_response_time,calculate_fulfilment_rate
# Create your models here.

class Vendors(models.Model):
    name = models.CharField(max_length=200,verbose_name="Vendor's name")
    contact_details = models.TextField(verbose_name="Contact information of the vendor")
    address = models.TextField(verbose_name="Physical address of the vendor")
    vendor_code = models.CharField(max_length=500,unique=True,verbose_name="A unique identifier for the vendor")
    on_time_delivery_rate = models.FloatField(default=0,verbose_name=" Tracks the percentage of on-time deliveries")
    quality_rating_avg = models.FloatField(default=0,verbose_name="Average rating of quality based on purchase orders")
    average_response_time = models.FloatField(default=0,verbose_name="Average time taken to acknowledge purchase orders")
    fulfillment_rate = models.FloatField(default=0,verbose_name="Percentage of purchase orders fulfilled successfully")
    

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=500,verbose_name="Unique number identifying the PO")
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE,verbose_name="Link to the vendor model")
    order_date = models.DateTimeField(verbose_name="Date when the order placed")
    expected_delivery_date = models.DateTimeField(verbose_name="Expected delivery date of the order")
    delivery_date = models.DateTimeField(verbose_name="Actual delivery date of the order")
    items = models.JSONField(verbose_name="Details of items ordered")
    quantity =models.IntegerField(verbose_name="total quantity of items in the PO")
    status = models.CharField(max_length=100,verbose_name="current status of the PO(e.g. pending, completed, canceled)")
    quality_rating = models.FloatField(verbose_name="rating given to the vendor for this PO",null=True,blank=True)
    issue_date = models.DateTimeField(verbose_name="Timestamp when the PO was issued to the vendor")
    acknowledgment_date = models.DateTimeField(null=True,blank=True,verbose_name="Timestamp when the vendor acknowledged the PO")
    
class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(Vendors,on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,verbose_name="Date of the Performance record")
    on_time_delivery_rate = models.FloatField(verbose_name="Historical record of the on-time delivery rate")
    quality_rating_avg = models.FloatField(verbose_name="Historical record of the quality rating average")
    average_response_time = models.FloatField(verbose_name="Historical record of the average response time.")
    fulfillment_rate = models.FloatField(verbose_name="Historical record of the fulfilment rate")
    
    
    
    
@receiver(post_save,sender = PurchaseOrder)
def update_vendor_performance(sender,instance,created,**kwargs):
    calculate_on_time_delivery_rate(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel)
    calculate_quality_rating_average(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel)
    calculate_avg_response_time(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel)
    
    
@receiver(pre_save,sender = PurchaseOrder)
def update_vendor_fulfilment_performance(sender,instance,**kwargs):
    calculate_fulfilment_rate(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel)