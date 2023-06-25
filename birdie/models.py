from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from admindash.models import Order


# Create your models here.

class BirdieOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
         return str(self.order)
    

