from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
import pytz


TYPE = (
    ('Essay', 'Essay'),
    ('Research_Paper', 'Research Paper'),
    
)

MARITAL_STATUS= (

    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
    
)

AREA= (

    ('Accounting', 'Accounting'),
    ('Finance', 'Finance'),
)

ALEVEL= (

    ('High_School', 'High School'),
    ('College', 'College'),
    
)

LANGUAGE= (

    ('English_UK', 'English UK'),
    ('English_US', 'English US'),
   
)

SPACING= (

    ('Single', 'Single'),
    ('Double', 'Double'),
   
)

STYLE= (

    ('APA', 'APA'),
    ('MLA', 'MLA'),
   
)

WLEVEL= (

    ('Standard', 'Standard'),
    ('Premuim', 'premium'),
   
)

STATUS= (
    
    ('Not_Paid', 'Not Paid'),
    ('Paid', 'Paid'),
    ('Approved', 'Approved'),
    ('Completed', 'Completed'),
    ('Bidding', 'Bidding'),
    ('Assigned', 'Assigned'),
    ('Editing', 'Editing'),
    ('Revision', 'Revision'),
    ('In_Progress', 'In Progress'),
    ('Cancelled', 'Cancelled'),
     
)

PAID= (

    ('Paid', 'Paid'),
    ('Not_Paid', 'Not Paid'),
    
)

SITE= (

    ('Birdie', 'Birdie'),
    ('Nursing', 'Nursing'),
    ('EXP', 'EXP'),
    
)

class Writer(models.Model):
    writer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancers")
    bio = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return str(self.writer)

class Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
         return str(self.client)

class Editor(models.Model):
    editor = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return str(self.editor)


class Order(models.Model):
    orderNo = models.IntegerField(default=100, null=True)
    order_type = models.CharField(max_length=50, null=False)
    subject_area = models.CharField(max_length=50, null=False)
    academic_level = models.CharField(max_length=50, null=False)
    language= models.CharField(max_length=50, null=False)
    deadline = models.DateTimeField(auto_now_add=False)
    pages= models.IntegerField(null=True)
    #words=models.IntegerField(null=True, default=1)
    spacing= models.CharField(max_length=50, null=False)
    sources=models.IntegerField(null=True, default=1)
    style=models.CharField(max_length=50, null=False)
    writer_level= models.CharField(max_length=50, null=False)
    title= models.CharField(max_length=50, null=False)
    description=models.TextField(blank=True, max_length=5000,)
    client = models.ForeignKey(Client, related_name= "customers", on_delete=models.CASCADE, null=True, blank=True)
    editor = models.ForeignKey(Editor, related_name= "helpers", on_delete=models.CASCADE, null=True, blank=True)
    writer = models.ForeignKey(Writer, related_name= "birdies", on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices= STATUS, default='Not_Paid')
    website = models.CharField(max_length=50, choices= SITE, default='Birdie')
    Submissiondate=models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=250)
    new_deadline = models.DateTimeField(auto_now_add=False, null=True)
    UpdationDate = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    writer_amount=models.IntegerField(null=True, default=1)
    editor_amount=models.IntegerField(null=True, default=1)
    net_amount=models.IntegerField(null=True, default=1)
    writer_time=models.DateTimeField(auto_now_add=False, null=True)
    rating=models.IntegerField(null=True, default=1)

    transaction_id=models.IntegerField(default=100000000, null=True)
    payment_date=models.DateTimeField(auto_now_add=True)

  

    class Meta:
            ordering = ['deadline']

    def save(self, *args, **kwargs):
        if self.academic_level  == 'high' or self.academic_level  == 'freshman':
            self.price = int(11) * int((self.pages))
        elif self.academic_level  == 'sophomore' or self.academic_level  == 'junior' or self.academic_level  == 'masters':
            self.price = int(13)* int((self.pages))
        elif self.academic_level == 'senior' or self.academic_level  == 'masters':
            self.price = int(14)* int((self.pages))

        elif self.academic_level  == 'doctoral':
            self.price = int(16)* int((self.pages))


        if self.writer_level == 'standard':
            self.price += int(2)
        elif self.writer_level == 'premium':
            self.price += int(5)
        elif self.writer_level == 'platinum':
            self.price += int(7)
        
        self.writer_amount = self.price * 0.3 
        self.editor_amount= self.price * 0.1  
        self.net_amount = self.price * 0.6 
        

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.academic_level} ({self.writer_level}): {self.price}"


    def __str__(self):
        return self.title


class Dashorderdetails(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    client = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name="admin_writer")
    
    order_amount=models.IntegerField(null=True, default=1)
    writer_amount=models.IntegerField(null=True, default=1)
    editor_amount=models.IntegerField(null=True, default=1)
    net_amount=models.IntegerField(null=True, default=1)
    status = models.CharField(max_length=50, choices= STATUS, null=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.order.title


class AdminOrderFile(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='adminfiles')
    file = models.FileField()
    file_status = models.CharField(max_length=50, null=False, default="draft")
    status = models.CharField(max_length=50, null=False, default="completed")
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True, blank=True, related_name="admin_editor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)


class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    file = models.FileField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Ordertracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    remark = models.CharField(max_length=1000, null=False)
    status = models.CharField(max_length=250, null=False)
    UpdationDate = models.DateTimeField(auto_now_add=True)
    rating=models.IntegerField(null=True, default=1)
    new_deadline = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.order.title


class StatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.order} status changed from {self.old_status} to {self.new_status} on {self.date}'

 
class ChatMessage(models.Model):

    ORDER_MSG_TYPE = (
        ('writer', 'Writer'),
        ('client', 'Client'),
        ('support', 'Support/Editor'),

    )

    SENDER_TYPE = (
        ('writer', 'Writer'),
        ('client', 'Client'),
        ('support', 'Support/Editor'),

    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE, default="client")
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, default="1", related_name='chat_recipient')
    recipient_type = models.CharField(max_length=10, choices=ORDER_MSG_TYPE, default="client")
    body = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return f"{self.sender.username} ({self.timestamp.strftime('%m/%d/%Y %H:%M:%S')})"
