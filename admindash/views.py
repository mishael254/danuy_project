from django.db import models
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.views import View
from django.contrib import messages
from .models import Order, Ordertracking, OrderFile, Writer, ChatMessage
from writers.models import Bid, Writer, WriterOrderFile
from django.http import HttpResponse, Http404
from .models import Dashorderdetails, AdminOrderFile
from birdie.forms import OrderForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from .models import Order, Client, Ordertracking, ChatMessage, Client, Writer, Editor, StatusLog
from django.db.models import Avg
from django.http import HttpResponse, Http404
import os
from django.http import FileResponse
import mimetypes
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import AdminOrderFile
from django.core.mail import send_mail, EmailMessage
from django.core.mail import get_connection



# Create your views here.


def acade(request):

    return render(request, 'accounts/writerslogin.html',)


def admindashboard(request):
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60
            
    
    return render(request, 'admindash/dashboard.html', locals())
    
def get_remaining_time(order):
    deadline = order.writer_time
    current_time = datetime.now()
    time_diff = deadline - current_time
    return time_diff

def allorders(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    orders = Order.objects.all()

    totalorder = Order.objects.all().count()

    allorders_total= sum(order.price for order in orders )

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60
            
    return render(request, 'admindash/allorders.html', locals())

def get_writer(user):
    writer = get_object_or_404(Writer, writer=user)
    return writer

def adminorderdetails(request, id):

    order = Order.objects.get(id=id)
    orders = Order.objects.all()
    orders_count = orders.count()
    dashorderdetails = Dashorderdetails.objects.filter(order=order)
    reportcount = Dashorderdetails.objects.filter(order=order).count()
    files = OrderFile.objects.filter(order=order)
    filescount = OrderFile.objects.filter(order=order).count()

    statustracking = StatusLog.objects.filter(order=order)
    statuscount = StatusLog.objects.filter(order=order).count()

    totalorder = Order.objects.all().count()

    allorders_total= sum(order.price for order in orders )

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    bids = Bid.objects.filter(order=order)
    bids_count= bids.count()

    editor = Editor.objects.get(editor=request.user)

    writerfiles = WriterOrderFile.objects.filter(order=order)
    writerfilescount = writerfiles.count()

    adminfiles = AdminOrderFile.objects.filter(order=order)
    adminfilescount = AdminOrderFile.objects.filter(order=order).count()

    chat_history = ChatMessage.objects.filter(order=order).order_by('-timestamp')
    
    if request.method == 'POST':

        remark = request.POST['remark']
        new_deadline = request.POST['new_deadline']

        ordertrack=Ordertracking.objects.create(status="Revision", new_deadline=new_deadline, remark=remark, order=order)
        order.new_deadline = new_deadline
        order.status = "Revision"
        order.remark = remark
        order.save()

        return redirect('dashboard')

   
    return render(request,'admindash/orderdetails.html',  locals())



def adminedit_order(request, id):
    
    order = get_object_or_404(Order, id=id)

    orders = Order.objects.all()
    orders_count = orders.count()
    dashorderdetails = Dashorderdetails.objects.filter(order=order)
    reportcount = Dashorderdetails.objects.filter(order=order).count()
    files = OrderFile.objects.filter(order=order)
    filescount = OrderFile.objects.filter(order=order).count()

    totalorder = Order.objects.all().count()

    allorders_total= sum(order.price for order in orders )

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    if request.method == 'POST':

        order.title = request.POST.get('title')
        order.academic_level = request.POST.get('academic_level')
        order.order_type = request.POST.get('order_type')
        order.subject_area = request.POST.get('subject_area')
        order.pages = request.POST.get('pages')
        order.sources = request.POST.get('sources')
        order.language = request.POST.get('language')
        order.spacing = request.POST.get('spacing')
        order.style = request.POST.get('style')
        order.writer_level = request.POST.get('writer_level')
        order.description = request.POST.get('description')
        
        # Save the changes to the database
        order.save()

        # Show success message
        messages.success(request, 'Order updated successfully!')
        
        # Redirect to the order detail page
        return redirect('adminorderdetails', id=order.id)
    


    return render(request, 'admindash/editorder.html', locals())


def admindelete_order(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('admindashboard')
    return render(request, 'admindash/deleteorder.html', {'order': order})


def adminpending(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    paid_total= sum(order.price for order in paid )

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in not_paid:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60
    
    return render(request, 'admindash/pending.html',  locals())


def adminavailable(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    paid_total= sum(order.price for order in paid )

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in paid:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60


    return render(request, 'admindash/available.html',  locals())


def adminprogress(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in progress_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60


    return render(request, 'admindash/progress.html',  locals())

def admincompleted(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in completed_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60
    


    return render(request, 'admindash/completed.html',  locals())

def adminrevision(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in revision_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60


    return render(request, 'admindash/revision.html',  locals())


def admincancelled(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in cancelled_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60


    return render(request, 'admindash/cancelled.html',  locals())


def adminbids(request):

    bids = Bid.objects.all()
    bids_count =bids.count()

    bid_orders = Order.objects.filter(status='Bidding')
    bid_orders_count=bid_orders.count()
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
   
    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in bid_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60

    

    context = {
    'bids_count': bids_count,
    'bid_orders': bid_orders,
    'bid_orders_count': bid_orders_count,
    'totalorder': totalorder,
    'orders_count': orders_count,
    'paid_count': paid_count,
    'not_paid_count': not_paid_count,
    'completed_orders_count': completed_orders_count,
    'approved_orders_count': approved_orders_count,
    'revision_orders_count': revision_orders_count,
    'progress_orders_count': progress_orders_count,
    'cancelled_orders_count': cancelled_orders_count,
    'total': total,
    'now': now,
    'assigned_orders_count': assigned_orders_count,
    'assigned_orders_total': assigned_orders_total,
    'editing_orders_count': editing_orders_count,
    'editing_orders_total': editing_orders_total,
    'bid_orders_count': bid_orders_count,
    'approval_ordertracking': approval_ordertracking,
    'revision_ordertracking': revision_ordertracking,
    
    }


    return render(request, 'admindash/bids.html', context)

def adminorder_bids(request, id):
    order = Order.objects.get(id=id)
    bids = Bid.objects.filter(order=order)
    bids_count= bids.count()

    current_order = Order.objects.get(id=id)
    bid_orders = Order.objects.filter(status='Bidding', id=id)

    bid_orders_count=bid_orders.count()

    context = {

        'order': order, 
        'bids': bids, 
        'bids_count' : bids_count,
        'bid_orders' : bid_orders,
        'bid_orders_count' : bid_orders_count,
        'current_order' :  current_order,
    
    }
    
    return render(request, 'admindash/order_bids.html', context)

def assign_writer(request, order_id, writer_id):
    order = get_object_or_404(Order, id=order_id)
    writer = get_object_or_404(Writer, id=writer_id)
    editor = Editor.objects.get(editor=request.user)
    order.writer = writer
    order.editor = editor
    order.status = 'Assigned'
    order.save()
    
    # #Send an email to the writer
    # subject_writer = f'Order #{order.orderNo} Assigned'
    # message_writer = f'Dear {order.writer}, you have been assigned order #{order.orderNo}; "{order.title}".<br>'
    # message_writer += '------------------------<br>'
    # message_support += 'For more information, please login in your account at: topwritersadmin.com<br><br>'
    # message_support += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
    # message_support += 'Support Team!'
    # writer_from_email = settings.DEFAULT_FROM_EMAIL2
    # EMAIL_BACKEND2 = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
    #                 host='162.0.209.152', 
    #                 port=465, 
    #                 username='support@academiawriter.com', 
    #                 password='Nicaragua2020', 
    #                 use_ssl=True)
    # recipient_list_writer = [order.writer.writer.email]
    # send_mail(subject_writer, '', writer_from_email, recipient_list_writer, connection=EMAIL_BACKEND2, html_message=message_writer)
                          
                          
    # # Send an email to the support
    # subject_support = f'Order #{order.orderNo} Assigned'
    # message_support = f'Dear Dan Oyugi, you have assigned order #{order.orderNo}; "{order.title}" to {order.writer} <br>'
    # message_support += '------------------------<br>'
    # message_support += 'For more information, please login in your account at: topwritersadmin.com<br><br>'
    # message_support += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
    # message_support += 'Support Team!'
    # from_email = settings.DEFAULT_FROM_EMAIL
    # EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
    #                                        host='162.0.209.152', 
    #                                        port=465, 
    #                                        username='info@nursingassignmentservice.com', 
    #                                        password='shakushaku2030', 
    #                                        use_ssl=True)
    # recipient_list_support = ['doyugi21@gmail.com', 'rogerskinoti0@gmail.com']
    # send_mail(subject_support, '', from_email, recipient_list_support, connection=EMAIL_BACKEND, html_message=message_support)
    
    messages.success(request, f'Writer {writer} has been assigned to order {order}')
    
    return redirect('adminorderdetails', id=order.id)

def adminassigned(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned__orders_total=sum(order.price for order in assigned_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in assigned_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60


    return render(request, 'admindash/assigned.html',  locals())

def adminapproved(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned__orders_total=sum(order.price for order in assigned_orders)
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    for order in assigned_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60


    return render(request, 'admindash/approved.html',  locals())

def adminediting(request):

    totalorder = Order.objects.all().count()
    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()

    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    not_paid_total= sum(order.price for order in not_paid )

    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    completed_orders_total=sum(order.price for order in completed_orders)

    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    approved_orders_total=sum(order.price for order in approved_orders)

    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    revision_orders_total=sum(order.price for order in revision_orders)

    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    progress_orders_total=sum(order.price for order in progress_orders)

    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    cancelled_orders_total=sum(order.price for order in cancelled_orders)

    assigned_orders = Order.objects.filter(status="Cancelled")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    
    
    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in  editing_orders:
        if order.writer_time is None:
            order.time_remaining_days = None
            order.time_remaining_hours = None
            order.time_remaining_minutes = None
        else:
            writer_current_time = order.writer_time
            time_remaining = writer_current_time - now - timedelta(hours=3)
            order.time_remaining_days = time_remaining.days
            
            time_remaining_seconds = time_remaining.seconds
            order.time_remaining_hours = time_remaining_seconds // 3600
            order.time_remaining_minutes = (time_remaining_seconds % 3600) // 60

    return render(request, 'admindash/adminediting.html',  locals())


def admin_upload_files(request, id):
    order = get_object_or_404(Order, id=id)
    adminfiles = AdminOrderFile.objects.filter(order=order)
    adminfilescount = AdminOrderFile.objects.filter(order=order).count()
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_status = request.POST.get('file_status')
        editor = Editor.objects.get(editor=request.user)

        if file_status == "draft":
            admin_file_status = "editing"
        elif file_status == "final":
            admin_file_status = "completed"

        AdminOrderFile.objects.create(file=file, editor=editor, status=admin_file_status, file_status=file_status, order=order)

        if file_status == "draft":
            order.status = "Editing"
        elif file_status == "final":
            order.status = "Completed"
        
        order.editor=editor
        order.save()
        return redirect('adminorderdetails', id=order.id)
    
    context = {
        'order': order,
        'adminfiles': adminfiles,
        'adminfilescount': adminfilescount 
    }

    print(str(adminfiles))
    
    return render(request, 'admindash/uploadfiles.html', context)
    
def adminusers(request):
    
    clients = Client.objects.all() 
    clients_count =  clients.count()
    
    writers = Writer.objects.filter(is_approved=True)
    writers_count = writers.count()
    
    applicants = Writer.objects.filter(is_approved=False) 
    applicants_count =  applicants.count()
    
    editors = Editor.objects.all() 
    editors_count =  editors.count()
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    
    return render(request, 'admindash/users.html', locals())
    
def adminclients(request):
    
    clients = Client.objects.all() 
    clients_count =  clients.count()
    
    writers = Writer.objects.filter(is_approved=True)
    writers_count = writers.count()
    
    applicants = Writer.objects.filter(is_approved=False) 
    applicants_count =  applicants.count()
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    
    return render(request, 'admindash/clients.html', locals())

def adminactivewriters(request):
    
    writers = Writer.objects.filter(is_approved=True)
    writers_count = writers.count()
    
    applicants = Writer.objects.filter(is_approved=False) 
    applicants_count =  applicants.count()
    
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    
    return render(request, 'admindash/activewriters.html', locals())

def adminapplicants(request):
    
    writers = Writer.objects.filter(is_approved=True)
    writers_count = writers.count()
    
    applicants = Writer.objects.filter(is_approved=False) 
    applicants_count =  applicants.count()
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    
    return render(request, 'admindash/applicants.html', locals())

def admineditors(request):
    
    editors = Editor.objects.all() 
    editors_count =  editors.count()
    
    writers = Writer.objects.filter(is_approved=True)
    writers_count = writers.count()
    
    applicants = Writer.objects.filter(is_approved=False) 
    applicants_count =  applicants.count()
    
    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed')
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved")
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision")
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="In_Progress")
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled")
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    assigned_orders = Order.objects.filter(status="Assigned")
    assigned_orders_count=assigned_orders.count()
    assigned_orders_total=sum(order.price for order in assigned_orders)

    editing_orders = Order.objects.filter(status="Editing")
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
   
    bid_orders = Order.objects.filter(status='Bidding')

    bid_orders_count=bid_orders.count()

    approval_ordertracking = Ordertracking.objects.filter(status="Approved")
    revision_ordertracking = Ordertracking.objects.filter(status="Revision")
    
    
    
    return render(request, 'admindash/editors.html', locals())
    
    



def download_file(request, file_path):
    file = get_object_or_404(AdminOrderFile, file=file_path)
    file_url = file.file.url
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_url[1:])
    if os.path.exists(file_full_path):
        with open(file_full_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_full_path)
            return response
    raise Http404
