from django.db.models import F,Avg
from datetime import timedelta
def calculate_on_time_delivery_rate(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel):
    if instance.status.lower() == "completed":
        vendor = Vendors.objects.get(id=instance.vendor.id)
        total_completed = PurchaseOrder.objects.filter(vendor = vendor.id,status = "completed")
        total_completed_count = PurchaseOrder.objects.filter(vendor = vendor.id,status = "completed").count()
        good_delivery = total_completed.filter(delivery_date__lte = F('expected_delivery_date') ).count()
        if total_completed!=0:
            on_time_delivery_rate = good_delivery/total_completed_count
        
        # return on_time_delivery_rate
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()
        update_historical_performance(vendor,HistoricalPerformanceModel)
    

def calculate_quality_rating_average(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel):
    if instance.status.lower() == "completed":
        if instance.quality_rating:
            vendor = Vendors.objects.get(id=instance.vendor.id)
            quality_rating_average = PurchaseOrder.objects.filter(vendor=vendor.id,status="completed").aggregate(avg_quality_rating = Avg('quality_rating'))['avg_quality_rating']
            vendor.quality_rating_avg = quality_rating_average or 0
            vendor.save()
            update_historical_performance(vendor,HistoricalPerformanceModel)
        

def calculate_avg_response_time(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel):
    if instance.acknowledgment_date:
        vendor = Vendors.objects.get(id=instance.vendor.id)
        pos = PurchaseOrder.objects.filter(vendor=vendor.id,acknowledgment_date__isnull = False)
        response_time_list = [(po.acknowledgment_date-po.issue_date).seconds for po in pos]
        if response_time_list:
            avg_response_time = sum(response_time_list)/len(response_time_list)
            vendor.average_response_time = avg_response_time
            vendor.save()
            update_historical_performance(vendor,HistoricalPerformanceModel)
        

def calculate_fulfilment_rate(instance,Vendors,PurchaseOrder,HistoricalPerformanceModel):
    if instance.id is None:
        vendor = Vendors.objects.get(id=instance.vendor.id)
        pos = PurchaseOrder.objects.filter(vendor = vendor.id)
        total_number_pos = pos.count()+1
        number_of_success_pos = pos.filter(status="completed").count()
        if instance.status == "completed":
            number_of_success_pos += 1
        fulfilment_rate = number_of_success_pos/total_number_pos
        vendor.fulfillment_rate = fulfilment_rate
        vendor.save()
        update_historical_performance(vendor,HistoricalPerformanceModel)
    else:
        # print("Saved status: ",PurchaseOrder.objects.get(id=instance.id).status)
        # print("instance status: ",instance.status)
        if PurchaseOrder.objects.get(id=instance.id).status != instance.status:
            vendor = Vendors.objects.get(id=instance.vendor.id)
            pos = PurchaseOrder.objects.filter(vendor = vendor.id)
            total_number_pos = pos.count()
            number_of_success_pos = pos.filter(status="completed").count()
            if instance.status == "completed":
                number_of_success_pos += 1
            fulfilment_rate = number_of_success_pos/total_number_pos
            vendor.fulfillment_rate = fulfilment_rate
            vendor.save()
            update_historical_performance(vendor,HistoricalPerformanceModel)
        


def update_historical_performance(vendor,HistoricalPerformanceModel):
    HistoricalPerformanceModel.objects.create(vendor=vendor,on_time_delivery_rate = vendor.on_time_delivery_rate,quality_rating_avg = vendor.quality_rating_avg,average_response_time = vendor.average_response_time,fulfillment_rate = vendor.fulfillment_rate)
    


            
    