from django.db import models
import uuid
from django.db.models import Avg, Count, F, ExpressionWrapper, DurationField
from django.utils import timezone


# Create your models here.
class VendorModel(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()  
    address = models.TextField() 
    vendor_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #A unique identifier for the vendor.
    on_time_delivery_rate = models.FloatField(default=0) #Tracks the percentage of on-time deliveries.
    quality_rating_avg = models.FloatField(default=0)  # Average rating of quality based on purchase orders.
    average_response_time = models.FloatField(default=0)  # Average time taken to acknowledge purchase orders.
    fulfilment_rate = models.FloatField(default=0)    #Percentage of purchase orders fulfilled successfully.
    
    def __str__(self):
        return self.name
    
    
    def calculate_performance_metrics(self):
        # On-Time Delivery Rate
        completed_orders_count = self.purchaseorder_set.filter(status='completed').count()
        on_time_delivery_count = self.purchaseorder_set.filter(status='completed', delivery_date__lte=timezone.now()).count()
        if completed_orders_count > 0:
            self.on_time_delivery_rate = (on_time_delivery_count / completed_orders_count) * 100

        # Quality Rating Average
        completed_orders_with_rating = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        if completed_orders_with_rating.exists():
            self.quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']

        # Average Response Time
        response_time_expr = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
        average_response_time = self.purchaseorder_set.filter(acknowledgment_date__isnull=False).annotate(response_time=response_time_expr).aggregate(avg_response_time=Avg('response_time'))
        if average_response_time['avg_response_time']:
            self.average_response_time = average_response_time['avg_response_time'].total_seconds() / 60

        # Fulfilment Rate
        total_orders_count = self.purchaseorder_set.count()
        successful_orders_count = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False).count()
        if total_orders_count > 0:
            self.fulfillment_rate = (successful_orders_count / total_orders_count) * 100

        self.save()

    
class PuchaseorderModel(models.Model):
    po_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(VendorModel,on_delete=models.CASCADE) 
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=200)
    quality_rating = models.FloatField(null =True,blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null =True,blank=True)
        
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()




