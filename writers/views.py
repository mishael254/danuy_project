from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Writer, Bid, Work, Payment, WriterOrderFile
from admindash.models import Order, Ordertracking, OrderFile, Writer, ChatMessage
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from .forms import UploadForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.db.models import Avg
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.mail import get_connection

@login_required
def writerdashboard(request):
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()
   
    avg_rating = Order.objects.filter(writer=writer, status='Approved').aggregate(Avg('rating'))['rating__avg']

    if avg_rating is not None:
        avg_rating = round(avg_rating, 1)



    dash_orders = Order.objects.filter(Q(status='Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
    
    
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in dash_orders:
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


    return render(request, 'writers/dashboard.html', locals())
    




def filter_orders_by_level(request, level):
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()

    if level == 'all':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(academic_level=level)

    return render(request, 'writers/dashboard.html', locals())


def get_writer(user):
    writer = get_object_or_404(Writer, writer=user)
    return writer

def writerorder (request, id):
    order = Order.objects.get(id=id)
    orders = Order.objects.all()
    orders_count = orders.count()
    ordertracking = Ordertracking.objects.filter(order=order)
    reportcount = Ordertracking.objects.filter(order=order).count()
    files = OrderFile.objects.filter(order=order)
    filescount = OrderFile.objects.filter(order=order).count()
    order_files = OrderFile.objects.filter(order=order)

    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()
    
    writer = get_writer(request.user)

    writerfiles = WriterOrderFile.objects.filter(order=order)
    writerfilescount = writerfiles.count()

    # Check if the writer has already placed a bid for the order
    has_placed_bid = order.bids.filter(writer=writer).exists()
    has_upload_permission = any([wf.file_status != 'final' for wf in writerfiles])

    chat_history = ChatMessage.objects.filter(order=order).order_by('-timestamp')

    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

        
    
    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
    
    words = order.pages * 275
    
    now = datetime.now(pytz.timezone('Africa/Nairobi'))

    writer_current_time = order.writer_time
    time_remaining = writer_current_time - now - timedelta(hours=3)
    time_remaining_days = time_remaining.days
    time_remaining_seconds = time_remaining.seconds
    time_remaining_hours = time_remaining_seconds // 3600
    time_remaining_minutes = (time_remaining_seconds % 3600) // 60
    
    client_current_time = order.deadline
    client_time_remaining = client_current_time - now - timedelta(hours=3)
    client_time_remaining_days = client_time_remaining.days
    client_time_remaining_seconds = client_time_remaining.seconds
    client_time_remaining_hours = client_time_remaining_seconds // 3600
    client_time_remaining_minutes = (client_time_remaining_seconds % 3600) // 60

    
    context = {
        'order': order,
        'orders': orders,
        'words' : words,
        'orders_count': orders_count,
        'ordertracking' : ordertracking,
        'reportcount' :  reportcount,
        'files' :  files,
        'filescount' :  filescount,
        'order_files': order_files,
        'has_placed_bid' : has_placed_bid,
        'bids' : bids,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
        'bids_count' : bids_count,
        'writerfiles' : writerfiles, 
        'writerfilescount' :  writerfilescount,
        'has_upload_permission' : has_upload_permission, 
        'chat_history': chat_history,
         'orders': orders, 
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'approved_orders': approved_orders,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        
        'time_remaining':time_remaining,
        'time_remaining_days':time_remaining_days,
        'time_remaining_hours':time_remaining_hours,
        'time_remaining_seconds':time_remaining_seconds,
        'time_remaining_minutes':time_remaining_minutes,
        
        'client_time_remaining':client_time_remaining,
        'client_time_remaining_days':client_time_remaining_days,
        'client_time_remaining_hours':client_time_remaining_hours,
        'client_time_remaining_seconds':client_time_remaining_seconds,
        'client_time_remaining_minutes':client_time_remaining_minutes,
       
        
    }
   
    return render(request,'writers/orderdetails.html', context)

def writer_upload_files(request, id):
    order = get_object_or_404(Order, id=id)
    writerfiles = WriterOrderFile.objects.filter(order=order)
    writerfilescount = WriterOrderFile.objects.filter(order=order).count()

    if request.method == 'POST':
        file = request.FILES.get('file')
        file_status = request.POST.get('file_status')

        if file_status == "draft":
            writer_file = WriterOrderFile.objects.create(file=file, status="Assigned", file_status=file_status, order=order)
        elif file_status == "final":
            writer_file = WriterOrderFile.objects.create(file=file, status="Editing", file_status=file_status, order=order)
        
        order.status = writer_file.status
        order.save()
        # Send an email to the support
        subject_support = f'Order #{order.orderNo} File(s) Added'
        message_support = f'Dear Dan Oyugi, {order.writer} has uploaded file(s)- a {file_status} file to order #{order.orderNo}; "{order.title}"<br>'
        message_support += f'File Status: {file_status} <br>'
        message_support += '------------------------<br>'
        message_support += 'For more information, please login in your account at: topwritersadmin.com<br><br>'
        message_support += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
        message_support += 'Support Team!'
        from_email = settings.DEFAULT_FROM_EMAIL
        EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                                           host='162.0.209.152', 
                                           port=465, 
                                           username='info@nursingassignmentservice.com', 
                                           password='shakushaku2030', 
                                           use_ssl=True)
        recipient_list_support = ['doyugi21@gmail.com', 'rogerskinoti0@gmail.com']
        send_mail(subject_support, '', from_email, recipient_list_support, connection=EMAIL_BACKEND, html_message=message_support)
        
        
        return redirect('writerorder', id=order.id)

    context = {

        'order': order,
        'writerfiles': writerfiles,
        'writerfilescount': writerfilescount
    }


    return render(request, 'writers/upload_files.html', context)


@login_required
def edit_profile(request):
   
    if request.method == 'POST':
        writer.bio = request.POST.get('bio', '')
        writer.hourly_rate = request.POST.get('hourly_rate', '')
        writer.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('dashboard')
    context = {'writer': writer}
    return render(request, 'writers/edit_profile.html', context)

@login_required
def place_bid(request, id):

    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        writer = Writer.objects.get(writer=request.user)

        bid = Bid.objects.create(

            writer=writer,
            amount=amount,
            status="Bidding",
            order=order,
            
        )
        order.status = "Bidding"
        order.writer = writer
        order.save()

        return redirect('writerorder', id=order.id)

    return render(request, 'place_bid.html', {'order': order})


def bids(request):

    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

        
    
    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
    
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

        'bids': bids, 
        'writer' : writer,
        'bids_count' : bids_count,
        'bid_orders' : bid_orders,
        'bid_orders_count' : bid_orders_count,
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        
    }

    return render(request, 'writers/bids.html', context)

def assigned_orders(request):

    writer_id = request.user.id
    orders = Order.objects.filter(writer_id=writer_id, status='Assigned')
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(writer=writer, status='Assigned')
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
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
        
    
    context = {
        
        'orders': orders,      
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'progress_orders' : progress_orders,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
    
    
    }
    return render(request, 'writers/assigned.html', context)

def editing_orders(request):

    writer_id = request.user.id
    orders = Order.objects.filter(writer_id=writer_id, status='Editing')
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()  
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in editing_orders:
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
        'orders': orders, 
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'editing_orders': editing_orders,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        
        
    }
    return render(request, 'writers/editing.html', context)

def revision_orders(request):

    writer_id = request.user.id
    orders = Order.objects.filter(writer_id=writer_id, status='Revision')
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()


    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count() 
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
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
        
    
    context = {
        'orders': orders, 
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'revision_orders':  revision_orders,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        
    }
    return render(request, 'writers/revision.html', context)

def completed_orders(request):

    writer_id = request.user.id
    orders = Order.objects.filter(writer_id=writer_id, status='Completed')
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()  
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
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
        
    
    context = {
        'orders': orders, 
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'completed_orders':  completed_orders,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        
        
    }
    return render(request, 'writers/completed.html', context)

def approved_orders(request):

    writer_id = request.user.id
    orders = Order.objects.filter(writer_id=writer_id, status='Approved')
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
   
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
   

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)

    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in approved_orders:
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
        'orders': orders, 
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'approved_orders': approved_orders,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
    
    }

    return render(request, 'writers/approved.html', context)
    
def clients_comments(request):

    writer_id = request.user.id
    orders = Order.objects.filter(writer_id=writer_id, status='Approved')
    bids = Bid.objects.all()
    work = Work.objects.all()

    totalorder = Order.objects.all().count()

    orders = Order.objects.all() 
   
    paid = Order.objects.filter(status='Paid')
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid')
    not_paid_count = not_paid.count()
    
    writer = Writer.objects.get(writer=request.user)
    bids = Bid.objects.filter(writer=writer)
    bids_count =bids.count()

    bidding_orders = Order.objects.filter(status='Bidding', writer=writer)
    bidding_orders_count = bidding_orders.count()
    completed_orders = Order.objects.filter(status='Completed', writer=writer)
    completed_orders_count=completed_orders.count()
    approved_orders = Order.objects.filter(status="Approved", writer=writer)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", writer=writer)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(status="Assigned", writer=writer)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", writer=writer)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
   

    editing_orders = Order.objects.filter(status="Editing", writer=writer)
    editing_orders_count=editing_orders.count()
    editing_orders_total=sum(order.price for order in editing_orders)
    
    ordertracking = Ordertracking.objects.all()
    reportcount = ordertracking.count()

    bid_orders = Order.objects.filter(status='Bidding', bids__in=bids)

    bid_orders_count=bid_orders.count()
    
    dash_orders = Order.objects.filter(Q(status='Not_Paid') | Q(status='Bidding')).exclude(Q(status='Bidding', writer=writer))
    
    dash_orders_count=dash_orders.count()
    now = datetime.now(pytz.timezone('Africa/Nairobi'))
    
    for order in approved_orders:
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
        'orders': orders, 
        'totalorder': totalorder,
        'paid_count': paid_count,
        'not_paid_count': not_paid_count,
        'writer': writer,
        'dash_orders': dash_orders,
        'dash_orders_count': dash_orders_count,
        'bids_count': bids_count,
        'bidding_orders_count': bidding_orders_count,
        'completed_orders_count': completed_orders_count,
        'approved_orders_count': approved_orders_count,
        'revision_orders_count': revision_orders_count,
        'progress_orders_count': progress_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'total': total,
        'now': now,
        'editing_orders_count': editing_orders_count,
        'editing_orders_total': editing_orders_total,
        'approved_orders': approved_orders,
        'bid_orders': bid_orders,
        'bid_orders_count': bid_orders_count,
        'ordertracking': ordertracking,
        'reportcount': reportcount,
    
    }

    return render(request, 'writers/comments.html', context)
    

def order_filter(request):
    selected_level = request.GET.get('academic_level', None)
    if selected_level:
        filtered_orders = Order.objects.filter(academic_level__exact=selected_level)
    else:
        filtered_orders = Order.objects.all()
    
    orders_data = []
    for order in filtered_orders:
        orders_data.append({
            'id': order.id,
            'academic_level': order.academic_level,
            # Add more fields as needed
        })
    
    return JsonResponse({'orders': orders_data})
