from rest_framework import serializers
from .models import Vendors,PurchaseOrder
class vendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = '__all__'
        
    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance

class purchaseorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
            
        instance.save()
        return instance