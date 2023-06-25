from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from admindash.models import Order


# Create your models here.

class NursingOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
         return str(self.order)
    


class NursingContact(models.Model):
  
  first_name = models.CharField(max_length=200,blank=True)
  last_name = models.CharField(max_length=200, blank=True)
  email = models.CharField(max_length=100, blank=True)
  message = models.TextField(blank=True)
  website = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)
  
  def __str__(self):
    return self.first_name




class NursingTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed

    def __str__(self):
        return f"Transaction #{self.id}"


class NursingSamples(models.Model):
  
  sample_file= models.FileField()
  sample_title = models.CharField(max_length=200, blank=True)
  sample_type = models.CharField(max_length=200, blank=True)
  sample_pages = models.IntegerField(null=True, default=1)
  sample_body= models.TextField(blank=True)
  sample_urgency = models.IntegerField(null=True, default=1)
  sample_academic_level = models.TextField(blank=True)
  sample_style = models.TextField(blank=True, max_length=5000)
  sample_sources= models.IntegerField(null=True, default=1)
  sample_subject_area = models.CharField(max_length=50, null=False)
  sample_price = models.IntegerField(default=0)
  sample_writer_level = models.CharField(max_length=50, null=True)
  sample_date=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.sample_title