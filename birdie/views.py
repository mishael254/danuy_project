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
from .models import BirdieOrder
from django.http import FileResponse
from django.http import HttpResponse, Http404
import random
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

from admindash.models import AdminOrderFile, Order, Client, Writer, Editor, Ordertracking, OrderFile, ChatMessage

def index(request):

    return render(request, 'birdie/index.html',)


@login_required
def orderform(request):
    if request.method == 'POST':
        orderNo = str(random.randint(10000, 99999))
        order_type= request.POST['order_type']
        subject_area = request.POST['subject_area']
        academic_level = request.POST['academic_level']
        language = request.POST['language']
        deadline = request.POST['deadline']
        pages = request.POST['pages']
        spacing = request.POST['spacing']
        sources = request.POST['sources']
        style = request.POST['style']
        writer_level = request.POST['writer_level']
        title = request.POST['title']
        description = request.POST['description']
        client = Client.objects.get(client=request.user)
        website="Birdie"
        
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
            description=description,
            website=website,
            
        )
        birdie_order= BirdieOrder.objects.create(order=order)

        messages.success(request, 'Your order has been submitted successfully.')
        return redirect('dashboard')

    return render(request, 'birdie/orderform.html')




@login_required (login_url='login')
def order(request, id):
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
                            messages.success(request, "Order status updated to Approved.")
                    except ValueError:
                        # If rating is not an integer, show an error message
                        messages.error(request, "Please enter a valid rating.")
                        
        return redirect('dashboard')

    return render(request, 'birdie/order.html', {'order': order, 'orders_count': orders_count, 'ordertracking': ordertracking, 'reportcount': reportcount, 'files': files, 'filescount': filescount, 'chat_history': chat_history, 'adminfiles': adminfiles, 'adminfilescount': adminfilescount})



def add_files(request, id):

    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file_field'):
                OrderFile.objects.create(order=order, file=f)
                messages.success(request, 'File uploaded successfully!')
            return redirect('order', id=id)
    else:
        form = FileForm()
      
    return render(request, 'birdie/add_files.html', {'form': form, 'order': order})

@login_required (login_url='login')
def dashboard(request):

    client = Client.objects.get(client=request.user)
    orders = Order.objects.filter(client=client)
    
    orders_count = orders.count()
    paid = Order.objects.filter(status='Paid', client=client)
    paid_count = paid.count()
    not_paid = Order.objects.filter(status='Not_Paid', client=client)
    not_paid_count = not_paid.count()
    completed_orders = Order.objects.filter(status='Completed' , client=client)
    completed_orders_count=completed_orders.count()
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

    
    
    print(str(orders))


    context = {
        'orders': orders,
        'orders_count': orders_count,
        'not_paid' :  not_paid,
        'paid': paid,
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
        
    }
   

    return render(request,'birdie/dashboard.html', context)
    


def order_chat(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    client = order.client
    writer = order.writer
    editor = order.editor

    if request.method == 'POST':
        msg_to = request.POST.get('msg_to')
        msg_body = request.POST.get('msg_body')
        sender_type = None
        
        if msg_to == 'writer':
            recipient_user = writer.writer
            recipient_type = 'writer'
            sender_type = 'client' if request.user == client.client else 'editor'
        elif msg_to == 'client':
            recipient_user = request.user
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

    chat_history = ChatMessage.objects.filter(order=order).order_by('-timestamp')
    chat_messages = [{'text': msg.body, 'timestamp': msg.timestamp, 'sender_type': msg.sender_type} for msg in chat_history]
    context = {
        'order': order,
        'chat_history': chat_history,
    }

    if request.is_ajax():
        return JsonResponse({'chat_messages': chat_messages})
    else:
        return render(request, 'birdie/order.html', context)

def order_messages(request):
    
    messages = ChatMessage.objects.all().order_by('-timestamp')
    
    context = {
       
        'messages': messages,
    }

    return render(request,'birdie/messages.html', context)
