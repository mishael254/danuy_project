from django.db import models
from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .forms import OrderUpdateForm, FileForm
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from .models import NursingOrder, NursingContact
from django.http import FileResponse
from django.http import HttpResponse, Http404
import random
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import pytz
from django.core.mail import send_mail, EmailMessage
from django.core.mail import get_connection
import json
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.shortcuts import redirect
from django.utils import timezone
from .models import NursingSamples

from admindash.models import AdminOrderFile, Order, Client, Writer, Editor, Ordertracking, OrderFile, ChatMessage

def home(request):

    return render(request, 'nursing/index.html',)

def about(request):

    return render(request, 'nursing/about.html',)

def Reviews(request):

    return render(request, 'nursing/reviews.html',)

def upload_sample(request):
    if request.method == 'POST':
        sample_title = request.POST.get('sample_title')
        sample_type = request.POST.get('sample_type')
        sample_pages = request.POST.get('sample_pages')
        sample_body = request.POST.get('sample_body')
        sample_urgency = request.POST.get('sample_urgency')
        sample_academic_level = request.POST.get('sample_academic_level')
        sample_style = request.POST.get('sample_style')
        sample_sources = request.POST.get('sample_sources')
        sample_subject_area = request.POST.get('sample_subject_area')

        if sample_academic_level == 'high' or sample_academic_level == 'freshman':
            sample_price = int(11) * int(sample_pages)
        elif sample_academic_level == 'sophomore' or sample_academic_level == 'junior' or sample_academic_level == 'masters':
            sample_price = int(13) * int(sample_pages)
        elif sample_academic_level == 'senior' or sample_academic_level == 'masters':
            sample_price = int(14) * int(sample_pages)
        elif sample_academic_level == 'doctoral':
            sample_price = int(16) * int(sample_pages)

        sample_file = request.FILES['sample_file']

        NursingSamples.objects.create(
            sample_title=sample_title,
            sample_type=sample_type,
            sample_pages=sample_pages,
            sample_body=sample_body,
            sample_urgency=sample_urgency,
            sample_academic_level=sample_academic_level,
            sample_style=sample_style,
            sample_sources=sample_sources,
            sample_subject_area=sample_subject_area,
            sample_price=sample_price,
            sample_file=sample_file
        )
        return redirect('nursingsamples')
    else:
        return render(request, 'nursing/upload_sample.html')


def nursingsamples(request):
    samples = NursingSamples.objects.all()

    context = {
                'samples': samples,
                
            }

    return render(request, 'nursing/samples.html', context)

def nursingsample(request, id):
    sample = NursingSamples.objects.get(id=id)

    context = {
                'sample': sample,
                
            }
    return render(request, 'nursing/sample.html', context)

def services(request):
    
    return render(request, 'nursing/services.html')


def Contact_us(request):
    if request.method == 'POST':
       
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        message = request.POST['message']
        website ="Nursing"
        
        contact = NursingContact.objects.create(
            
            first_name = first_name,
            last_name = last_name,
            email = email,
            message = message,
            website= website,
            
        )
       
        messages.success(request, 'Your inqury has been submitted successfully.')
        return redirect('Contact_us')

    return render(request, 'nursing/contact_us.html')




@login_required(login_url='nursinglogin')
def nursingorderform(request):
    context = {}  # Define context with a default value
    if request.method == 'POST':
        orderNo = str(random.randint(10000, 99999))
        order_type= request.POST['order_type']
        subject_area = request.POST['subject_area']
        academic_level = request.POST['academic_level']
        language = request.POST['language']
        deadline_str = request.POST['deadline']
        pages = request.POST['pages']
        spacing = request.POST['spacing']
        sources = request.POST['sources']
        style = request.POST['style']
        writer_level = request.POST['writer_level']
        title = request.POST['title']
        description = request.POST['description']
        client = Client.objects.get(client=request.user)
        website="Nursing"
        
    

        # Convert the deadline string to a datetime object
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')

        current_time = datetime.now()
        time_diff = deadline - current_time

        # Calculate the writer time as 50% of the time difference
        writer_time_diff = time_diff * 0.5
        current_writer_time = current_time + writer_time_diff
        writer_time=current_writer_time + timedelta(hours=1, minutes=30)

        # Format the writer time as a string in the desired format
        # writer_time_str = writer_time.strftime('%B %d, %Y, %I:%M %p')

        time_remaining = deadline - writer_time

        # Create the order and nursing order objects
        order = Order.objects.create(
            order_type=order_type,
            client=client,
            subject_area=subject_area,
            orderNo=orderNo,
            academic_level=academic_level,
            language=language,
            deadline=deadline,
            pages=pages,
            spacing=spacing,
            sources=sources,
            style=style,
            writer_level=writer_level,
            title=title,
            writer_time=writer_time,
            description=description,
            website=website,

        )
        nursing_order= NursingOrder.objects.create(order=order)
        context = {
            'writer_time': writer_time,
            'time_remaining_days': int(time_remaining.days),
            'time_remaining_hours': int(time_remaining.seconds / 3600),
            'time_remaining_minutes': int((time_remaining.seconds % 3600) / 60),

        }
        # Send an email to the client
        subject_client = f'Order #{order.orderNo} created Successfully'
        message_client = f'Dear {client.client.first_name}, Your order has been created successfully.<br>'
        message_client += f'Order: #{order.orderNo}-"{order.title}".<br>'
        message_client += f'Instructions: {order.description}.<br>'
        message_client += f'Deadline: {order.deadline}.<br>'
        message_client += '------------------------<br>'
        message_client += 'For more information, please visit our website at: compellingessays.com<br>'
        #message_client += '<img src="https://nursingassignmentservice.com/wp-content/uploads/2021/06/NursingAssignmentService_logo.png" alt="Nursing Assignment Service" width="200px" height="50px" style="display:block;margin-top:20px;"><br><br>'
        message_client += 'The Compelling Essays Team!'
        client_from_email = settings.DEFAULT_FROM_EMAIL
        EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                        host='162.0.209.152', 
                        port=465, 
                        username='info@nursingassignmentservice.com', 
                        password='shakushaku2030', 
                        use_ssl=True)
        recipient_list_client = [order.client.client.email]
        send_mail(subject_client, '', client_from_email, recipient_list_client, connection=EMAIL_BACKEND, html_message=message_client)
                
        # Send an email to the support
        subject_support = f'Order #{order.orderNo} Placed'
        message_support = f'Dear Daniel, Client {client.client.first_name} has placed an order #{order.orderNo}; "{order.title}".<br>'
        message_support += f'Instructions: {order.description}.<br>'
        message_support += f'Deadline: {order.deadline}.<br>'
        message_support += f'Amount: {order.price}.<br>'
        message_support += '------------------------<br>'
        message_support += 'For more information, please login in your account at: compellingessays.com<br><br>'
        #message_support += '<img src="https://academiawriter.com/static/img/acadelogo.png" alt="Academia Writer" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
        message_support += 'Compelling Essays Support!'
        from_email = settings.DEFAULT_FROM_EMAIL
        EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                        host='162.0.209.152', 
                        port=465, 
                        username='info@nursingassignmentservice.com', 
                        password='shakushaku2030', 
                        use_ssl=True)
        recipient_list_support = ['doyugi21@gmail.com', 'rogerskinoti0@gmail.com']
        send_mail(subject_support, '', from_email, recipient_list_support, connection=EMAIL_BACKEND, html_message=message_support)
                       
        messages.success(request, 'Your order has been submitted successfully.')
        return redirect('Dashboard')

    else:
        # Render the order creation form
        return render(request, 'nursing/orderform.html', context)


# def nursingorderform(request):
#     if request.method == 'POST':
#         orderNo = str(random.randint(10000, 99999))
#         order_type= request.POST['order_type']
#         subject_area = request.POST['subject_area']
#         academic_level = request.POST['academic_level']
#         language = request.POST['language']
#         deadline_str = request.POST['deadline']
#         pages = request.POST['pages']
#         spacing = request.POST['spacing']
#         sources = request.POST['sources']
#         style = request.POST['style']
#         writer_level = request.POST['writer_level']
#         title = request.POST['title']
#         description = request.POST['description']
#         client = Client.objects.get(client=request.user)
#         website="Nursing"
        
#         # Convert the deadline string to a datetime object
#         deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')

#         current_time = datetime.now()
#         time_diff = deadline - current_time

#         # Calculate the writer time as 50% of the time difference
#         writer_time_diff = time_diff * 0.5
#         current_writer_time = current_time + writer_time_diff
#         writer_time=current_writer_time + timedelta(hours=1, minutes=30)

#         # Format the writer time as a string in the desired format
#         # writer_time_str = writer_time.strftime('%B %d, %Y, %I:%M %p')
        
#         time_remaining = deadline - writer_time

#         # Create the order and nursing order objects
#         order = Order.objects.create(
#             order_type=order_type,
#             client=client,
#             subject_area=subject_area,
#             orderNo=orderNo,
#             academic_level=academic_level,
#             language=language,
#             deadline=deadline,
#             pages=pages,
#             spacing=spacing,
#             sources=sources,
#             style=style,
#             writer_level=writer_level,
#             title=title,
#             writer_time=writer_time,
#             description=description,
#             website=website,
            
#         )
#         nursing_order= NursingOrder.objects.create(order=order)
#         context = {
#             'writer_time': writer_time,
#             'time_remaining_days': int(time_remaining.days),
#             'time_remaining_hours': int(time_remaining.seconds / 3600),
#             'time_remaining_minutes': int((time_remaining.seconds % 3600) / 60),
           
#         }

#         messages.success(request, 'Your order has been submitted successfully.')
#         return redirect('Dashboard')
        
       

#     return render(request, 'nursing/orderform.html')




@login_required(login_url='nursinglogin')
def nursingorder(request, id):
    order = Order.objects.get(id=id)
    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    orders_count = orders.count()
    ordertracking = Ordertracking.objects.filter(order=order)
    reportcount = Ordertracking.objects.filter(order=order).count()
    files = OrderFile.objects.filter(order=order)
    filescount = OrderFile.objects.filter(order=order).count()
    chat_history = ChatMessage.objects.filter(order=order).order_by('-timestamp')

    adminfiles = AdminOrderFile.objects.filter(order=order)
    adminfilescount = AdminOrderFile.objects.filter(order=order).count()
    
    client = Client.objects.get(client=request.user)
    #editor = Editor.objects.get(editor=request.user)
    #writer = Writer.objects.get(writer=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    
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
    
    # Get count of unread messages for the current user
    if request.user == client.client:
        unread_count = ChatMessage.objects.filter(order=order, recipient_user=client.client, sender_type__in=['writer', 'support'], read=False).count()
    elif request.user == writer.writer:
        unread_count = ChatMessage.objects.filter(order=order, recipient_user=writer.writer, sender_type__in=['client', 'support'], read=False).count()
    elif request.user == editor.editor:
        unread_count = ChatMessage.objects.filter(order=order, recipient_user=editor.editor, sender_type__in=['client', 'writer'], read=False).count()
    else:
        unread_count = 1
    
    # Mark all unread messages for the current user as read
    ChatMessage.objects.filter(order=order, recipient_user=request.user, read=False).update(read=True)
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()
    
    if request.method == 'POST':
        print(request.POST)
        remark = request.POST.get('remark', '')
        new_deadline = request.POST.get('new_deadline', '')
        status = request.POST.get('status', '')

        if status == "Revision":
            if not remark or not new_deadline:
                # If remark or new_deadline is missing, show an error message
                messages.error(request, "Please enter a remark and a new deadline.")
            else:
                order.status = "Revision"
                order.remark = remark
                order.new_deadline = new_deadline
                order.save()
                Ordertracking.objects.create(status=status, new_deadline=new_deadline, remark=remark, order=order)
                
                # Send an email to the client
                subject_client = f'Order #{order.orderNo} sent for revision'
                message_client = f'Dear {client.client.first_name}, We have forwarded your revision request to the writer. Please await their response.<br>'
                message_client += f'Order: #{order.orderNo}-"{order.title}".<br>'
                message_client += f'Revision Instructions: {order.remark}.<br>'
                message_client += f'New Deadline: {order.new_deadline}.<br>'
                message_client += '------------------------<br>'
                message_client += 'For more information, please visit our website at: compellingessays.com<br>'
                message_client += '<img src="https://compellingessays.com/static/img/compellinglogo.png" alt="Compelling Essays" width="200px" height="50px" style="display:block;margin-top:20px;"><br><br>'
                message_client += 'The Support Team!'
                client_from_email = settings.DEFAULT_FROM_EMAIL
                EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                               host='162.0.209.152', 
                               port=465, 
                               username='info@nursingassignmentservice.com', 
                               password='shakushaku2030', 
                               use_ssl=True)
                recipient_list_client = [order.client.client.email]
                send_mail(subject_client, '', client_from_email, recipient_list_client, connection=EMAIL_BACKEND, html_message=message_client)
                
                # Send an email to the writer
                subject_writer = f'Revision on order #{order.orderNo}'
                message_writer = f'Dear {order.writer}, Client has requested revision for order #{order.orderNo}; "{order.title}".<br>'
                message_writer += f'Revision Instructions: {order.remark}.<br>'
                message_writer += f'New Deadline: {order.new_deadline}.<br>'
                message_writer += '------------------------<br>'
                message_writer += 'For more information, please login in your account at: topwritersadmin.com/writers/writerdashboard<br><br>'
                message_writer += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
                message_writer += 'Top Writers Admin Support!'
                writer_from_email = settings.DEFAULT_FROM_EMAIL2
                EMAIL_BACKEND2 = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                               host='162.0.209.152', 
                               port=465, 
                               username='support@academiawriter.com', 
                               password='Nicaragua2020', 
                               use_ssl=True)
                recipient_list_writer = [order.writer.writer.email]
                send_mail(subject_writer, '', writer_from_email, recipient_list_writer, connection=EMAIL_BACKEND2, html_message=message_writer)
                
                # Send an email to the support
                subject_support = f'Revision on order #{order.orderNo}'
                message_support = f'Dear Dan Oyugi, Client has requested revision for order #{order.orderNo}; "{order.title}".<br>'
                message_support += f'Revision Instructions: {order.remark}.<br>'
                message_support += f'New Deadline: {order.new_deadline}.<br>'
                message_support += '------------------------<br>'
                message_support += 'For more information, please login in your account at: topwritersadmin.com<br><br>'
                message_support += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
                message_support += 'Top Writers Admin Support!'
                from_email = settings.DEFAULT_FROM_EMAIL
                EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                               host='162.0.209.152', 
                               port=465, 
                               username='info@nursingassignmentservice.com', 
                               password='shakushaku2030', 
                               use_ssl=True)
                recipient_list_support = ['doyugi21@gmail.com', 'rogerskinoti0@gmail.com']
                send_mail(subject_support, '', from_email, recipient_list_support, connection=EMAIL_BACKEND, html_message=message_support)
                
                messages.success(request, "Order status updated to Revision.")
        elif status == "Approved":
            if not remark:
                # If remark is missing, show an error message
                messages.error(request, "Please enter a remark.")
            else:
                rating = request.POST.get('rating', '')
                if not rating:
                    # If rating is missing, show an error message
                    messages.error(request, "Please enter a rating.")
                else:
                    try:
                        rating = int(rating)
                        if rating < 1 or rating > 5:
                            # If rating is out of range, show an error message
                            messages.error(request, "Please enter a rating between 1 and 5.")
                        else:
                            order.status = "Approved"
                            order.remark = remark
                            order.rating = rating
                            order.save()
                            Ordertracking.objects.create(status=status, remark=remark, rating=rating, order=order)
                            # Send an email to the client
                            subject_client = f'Order #{order.orderNo} Approved'
                            message_client = f'Dear {client.client.first_name}, You have approved and cleared the order.<br>'
                            message_client += f'Order: #{order.orderNo}-"{order.title}".<br>'
                            message_client += f'Comment: {order.remark}.<br>'
                            message_client += f'Rating: {order.rating}.<br>'
                            message_client += '------------------------<br>'
                            message_client += 'For more information, please visit our website at: compellingessays.com<br>'
                            message_client += '<img src="https://compellingessays.com/static/compellinglogo.png" alt="Compelling Essays" width="200px" height="50px" style="display:block;margin-top:20px;"><br><br>'
                            message_client += 'The Nursing Team!'
                            client_from_email = settings.DEFAULT_FROM_EMAIL
                            EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                                           host='162.0.209.152', 
                                           port=465, 
                                           username='info@nursingassignmentservice.com', 
                                           password='shakushaku2030', 
                                           use_ssl=True)
                            recipient_list_client = [order.client.client.email]
                            send_mail(subject_client, '', client_from_email, recipient_list_client, connection=EMAIL_BACKEND, html_message=message_client)
                            
                            # Send an email to the writer
                            subject_writer = f'Order #{order.orderNo} Approved'
                            message_writer = f'Dear {order.writer}, Client has approved order #{order.orderNo}; "{order.title}".<br>'
                            message_writer += f'Comments: {order.remark}.<br>'
                            message_writer += f'Rating: {order.rating}.<br>'
                            message_writer += '------------------------<br>'
                            message_writer += 'For more information, please login in your account at: topwritersadmin.com/writers/writerdashboard<br><br>'
                            message_writer += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;">\n\n\n\n\n\n\n\n\n'
                            message_writer += 'Academia Writer Support!'
                            writer_from_email = settings.DEFAULT_FROM_EMAIL2
                            EMAIL_BACKEND2 = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                                           host='162.0.209.152', 
                                           port=465, 
                                           username='support@academiawriter.com', 
                                           password='Nicaragua2020', 
                                           use_ssl=True)
                            recipient_list_writer = [order.writer.writer.email]
                            send_mail(subject_writer, '', writer_from_email, recipient_list_writer, connection=EMAIL_BACKEND2,  html_message=message_writer)
                            
                            # Send an email to the support
                            subject_support = f'Order #{order.orderNo} Approved'
                            message_support = f'Dear Dan Oyugi, Client has approved order #{order.orderNo}; "{order.title}".<br>'
                            message_support += f'Comments: {order.remark}.<br>'
                            message_support += f'Rating: {order.rating}.<br>'
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

                            messages.success(request, "Order status updated to Approved.")
                    except ValueError:
                        # If rating is not an integer, show an error message
                        messages.error(request, "Please enter a valid rating.")
                    
                       
        return redirect('Dashboard')

    return render(request, 'nursing/order.html', {'order': order, 'orders': orders,
        'orders_count': orders_count,'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'writer_current_time': writer_current_time,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'orders_count': orders_count, 
        'ordertracking': ordertracking, 
        'reportcount': reportcount, 
        'files': files, 
        'filescount': filescount, 
        'chat_history': chat_history, 
        'adminfiles': adminfiles, 
        'unread_count': unread_count,
        
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
        'site_messages' : site_messages,
        'messages_count' : messages_count,
        
        
        'adminfilescount': adminfilescount,})


@login_required(login_url='nursinglogin')
def nursing_add_files(request, id):
    order = get_object_or_404(Order, id=id)
    client = Client.objects.get(client=request.user)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file_field'):
                OrderFile.objects.create(order=order, file=f)
                messages.success(request, 'File uploaded successfully!')
            return redirect('nursingorder', id=id)
    else:
        form = FileForm()
        # Send an email to the client
        subject_client = f'Order #{order.orderNo} File(s) Added'
        message_client = f'Dear {client.client.first_name}, You have added file(s) to #{order.orderNo}; "{order.title}"<br>'
        message_client += '------------------------<br>'
        message_client += 'For more information, please visit our website at: compellingessays.com<br>'
        message_client += '<img src="https://compellingessays.com/static/img/compellinglogo.png" alt="Compelling Essays" width="200px" height="50px" style="display:block;margin-top:20px;"><br><br>'
        message_client += 'The Support Team!'
        client_from_email = settings.DEFAULT_FROM_EMAIL
        EMAIL_BACKEND = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                                           host='162.0.209.152', 
                                           port=465, 
                                           username='info@nursingassignmentservice.com', 
                                           password='shakushaku2030', 
                                           use_ssl=True)
        recipient_list_client = [client.client.email]
        send_mail(subject_client, '', client_from_email, recipient_list_client, connection=EMAIL_BACKEND, html_message=message_client)
                            
        # Send an email to the writer
        subject_writer = f'Order #{order.orderNo} File(s) Added'
        if order.writer and order.writer.writer:
            recipient_list_writer = [order.writer.writer.email]
            message_writer = f'Dear {order.writer}, client has added file(s) to order #{order.orderNo}; "{order.title}"<br>'
            message_writer += '------------------------<br>'
            message_writer += 'For more information, please login in your account at: topwritersadmin.com<br><br>'
            message_writer += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Top Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;"><br>'
            message_writer += 'Support Team!'
            writer_from_email = settings.DEFAULT_FROM_EMAIL2
            EMAIL_BACKEND2 = get_connection(backend='django.core.mail.backends.smtp.EmailBackend', 
                                               host='162.0.209.152', 
                                               port=465, 
                                               username='support@academiawriter.com', 
                                               password='Nicaragua2020', 
                                               use_ssl=True)
            send_mail(subject_writer, '', writer_from_email, recipient_list_writer, connection=EMAIL_BACKEND2, fail_silently=True, html_message=message_writer)
        else:
            print("Writer not found, email not sent.")
        
        # Send an email to the support
        subject_support = f'Order #{order.orderNo} File(s) Added'
        message_support = f'Dear Dan Oyugi, client has added file(s) to order #{order.orderNo}; "{order.title}"<br>'
        message_support += '------------------------<br>'
        message_support += 'For more information, please login in your account at: topwritersadmin.com<br><br>'
        message_support += '<img src="https://topwritersadmin.com/static/img/adminlogo.png" alt="Writers Admin" width="200px" height="50px" style="display:block;margin-top:20px;"><br>'
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
        

    return render(request, 'nursing/add_files.html', {'form': form, 'order': order})


@login_required(login_url='nursinglogin')  
def nursingpayment(request,  id):
    
    order = Order.objects.get(id=id)
    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    orders_count = orders.count()

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()

    
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()

    context = {
        'order': order,
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages' : site_messages,
        'messages_count': messages_count,
       
    }
   
    return render(request,'nursing/payment.html', context)



def update_order_status(request, order_id):
    
    if request.method == 'GET':
        # Assuming you have an Order model with fields like transaction_id, status, and payment_date
        transaction_id = random.randint(1000000000, 9999999999)  # Generate a random transaction ID
        status = 'Paid'  # Set the status to 'paid'
        payment_date = timezone.now()  # Set the payment date to the current date and time

        # Retrieve the order based on the provided ID or return a 404 error if it doesn't exist
        order = get_object_or_404(Order, id=order_id)

        # Update the order status, transaction ID, and payment date in your database or perform any necessary actions
        order.transaction_id = transaction_id
        order.status = status
        order.payment_date = payment_date
        order.save()

        # Redirect to the dashboard page or replace 'dashboard' with the appropriate URL name
        return redirect('Dashboard')

    return JsonResponse({'message': 'Invalid request method.'}, status=400)





@login_required(login_url='nursinglogin')
def Dashboard(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()

    
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()
    
    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages' : site_messages,
        'messages_count': messages_count,
       
        
        
    }
   

    return render(request,'nursing/dashboard.html', context)


@login_required(login_url='nursinglogin')
def nursing_transactions(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()

    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count' :  messages_count,
        
    }
   

    return render(request,'nursing/transactions.html', context)
    

@login_required(login_url='nursinglogin')
def nursing_bidding(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()

    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count' : messages
        
    }
   

    return render(request,'nursing/bidding.html', context)

@login_required(login_url='nursinglogin')
def nursing_paid(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()

    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count' : messages_count,
        
    }
   

    return render(request,'nursing/paid.html', context)
    
def nursing_inprogress(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()


    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count':messages_count
        
    }

    return render(request,'nursing/inprogress.html', context)
    
def nursing_completed(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()


    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count': messages_count
        
    }
   

    return render(request,'nursing/completed.html', context)

def nursing_revision(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()

    

    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count':messages_count
        
    }
   

    return render(request,'nursing/revision.html', context)
    
def nursing_approved(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()
    
    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
    ).order_by('-timestamp')

    messages_count = site_messages.count()

    


    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'site_messages': site_messages,
        'messages_count': messages_count
        
    }

    return render(request,'nursing/approved.html', context)


@login_required(login_url='nursinglogin')
def order_chat(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    client = order.client
    writer = order.writer
    editor = order.editor

    if request.method == 'POST':
        msg_to = request.POST.get('msg_to')
        msg_body = request.POST.get('msg_body')
        sender_type = None
        
        # Check if sender is trying to send a message to themselves
        if request.user == client.client and msg_to == 'client':
            return JsonResponse({'success': False, 'error': 'Invalid recipient'})
        elif request.user == writer.writer and msg_to == 'writer':
            return JsonResponse({'success': False, 'error': 'Invalid recipient'})
        elif request.user == editor.editor and msg_to == 'support':
            return JsonResponse({'success': False, 'error': 'Invalid recipient'})

        if msg_to == 'writer':
            recipient_user = writer.writer
            recipient_type = 'writer'
            sender_type = 'client' if request.user == client.client else 'editor'
        elif msg_to == 'client':
            recipient_user = client.client
            recipient_type = 'client'
            sender_type = 'writer' if request.user == writer.writer else 'editor'
        elif msg_to == 'support':
            recipient_user = editor.editor
            recipient_type = 'support'
            sender_type =  'writer' if request.user == writer.writer else 'client'
        else:
            return JsonResponse({'success': False, 'error': 'Invalid recipient_type'})

        msg = ChatMessage(sender=request.user, sender_type=sender_type, recipient_user=recipient_user, recipient_type=recipient_type, order=order, body=msg_body)
        msg.save()

        return JsonResponse({'success': True})

    # Get chat history for the current order
    chat_history = ChatMessage.objects.filter(order=order).order_by('-timestamp')
    
    # Get count of unread messages for the current user
    if request.user == client.client:
        unread_count = ChatMessage.objects.filter(order=order, recipient_user=client.client, sender_type__in=['writer', 'support'], read=False).count()
    elif request.user == writer.writer:
        unread_count = ChatMessage.objects.filter(order=order, recipient_user=writer.writer, sender_type__in=['client', 'support'], read=False).count()
    elif request.user == editor.editor:
        unread_count = ChatMessage.objects.filter(order=order, recipient_user=editor.editor, sender_type__in=['client', 'writer'], read=False).count()
    else:
        unread_count = 0
    
    # Mark all unread messages for the current user as read
    ChatMessage.objects.filter(order=order, recipient_user=request.user, read=False).update(read=True)

    context = {
        'order': order,
        'chat_history': chat_history,
        'unread_count': unread_count,
    }

    if request.is_ajax():
        chat_messages = [{'text': msg.body, 'timestamp': msg.timestamp, 'sender_type': msg.sender_type} for msg in chat_history]
        return JsonResponse({'chat_messages': chat_messages})
    else:
        return render(request, 'nursing/order.html', context)

        


@login_required(login_url='nursinglogin')
def nursing_order_messages(request):
    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
    bidding_orders = Order.objects.filter(status='Bidding' , client=client)
    bidding_orders_count=bidding_orders.count()
    approved_orders = Order.objects.filter(status="Approved", client=client)
    approved_orders_count=approved_orders.count()
    revision_orders = Order.objects.filter(status="Revision", client=client)
    revision_orders_count=revision_orders.count()
    progress_orders = Order.objects.filter(Q(status='Assigned') | Q(status='Editing'), client=client)
    progress_orders_count=progress_orders.count()
    cancelled_orders = Order.objects.filter(status="Cancelled", client=client)
    cancelled_orders_count=cancelled_orders.count()
    total = Order.objects.aggregate(total=models.Sum('price'))['total']
    now = datetime.now()

   

    site_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient_user=request.user)
     ).order_by('-timestamp')

    messages_count = site_messages.count()
    
    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'not_paid_count': not_paid_count,
        'paid': paid,
        'paid_count': paid_count,
        'completed_orders' : completed_orders, 
        'completed_orders_count' :completed_orders_count,
        'revision_orders' : revision_orders,
        'revision_orders_count' : revision_orders_count,
        'progress_orders' : progress_orders,
        'progress_orders_count' : progress_orders_count,
        'cancelled_orders' : cancelled_orders,
        'cancelled_orders_count' : cancelled_orders_count,
        'total': total,
        'approved_orders' : approved_orders,
        'approved_orders_count' : approved_orders_count,
        'client':  client,
        'bidding_orders': bidding_orders,
        'bidding_orders_count': bidding_orders_count,
        'messages_count': messages_count 
        
    }

    return render(request,'nursing/messages.html', context)
