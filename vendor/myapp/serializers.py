from rest_framework import serializers
from .models import VendorModel,PuchaseorderModel,HistoricalPerformance
from django.contrib.auth.models import User

class VendorSerializer(serializers.ModelSerializer):
    class Meta():
        model = VendorModel
        fields = '__all__'
        
class PurchaseorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuchaseorderModel
        fields = '__all__'
        
class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance 
        fields = '__all__'    
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','username','password','email']            
        
                