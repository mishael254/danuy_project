from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from admindash.models import Order, Writer, Editor


file_choices = (

    ('Draft', 'Draft'),
    ('Final', 'Final'),
    
)


class Bid(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='bids')
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, blank=True, null=True)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, blank=True, null=True, related_name='bids')
    amount = models.CharField(max_length=20, default="Bidding this order")
    status = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f" Bid by {self.writer} - for order {self.order} - @ {self.amount} usd"

class Work(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Assigned")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.order.title

class Payment(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.writer.user.username} - {self.amount}"


class WriterOrderFile(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='workfiles')
    file = models.FileField()
    file_status = models.CharField(max_length=50, null=False, default="draft")
    status = models.CharField(max_length=50, null=False, default="editing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)