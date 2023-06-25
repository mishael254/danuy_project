from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('Reviews',views.Reviews, name='Reviews'),
    path('Contact_us',views.Contact_us, name='Contact_us'),
    path('upload-sample/', views.upload_sample, name='upload_sample'),
    path('nursingsamples',views.nursingsamples, name='nursingsamples'),
     path('services',views.services, name='services'),
    path('nursingsample/<int:id>/', views.nursingsample, name='nursingsample'),

    path('form/', views.nursingorderform, name='nursingorderform'),
    path('corder/<int:id>/', views.nursingorder, name='nursingorder'),
    path('payment/<int:id>/', views.nursingpayment, name='nursingpayment'),
    
    path('Dashboard', views.Dashboard, name='Dashboard'),
    
    path('cadd_files/<int:id>/', views.nursing_add_files, name='nursing_add_files'),
    
    path('order/<int:order_id>/chat/', views.order_chat, name='order_chat'),
    path('messages/', views.nursing_order_messages, name='nursing_order_messages'),
    path('bidding', views.nursing_bidding, name='nursing_bidding'),
    path('progress', views.nursing_inprogress, name='nursing_inprogress'),
    path('completed', views.nursing_completed, name='nursing_completed'),
    path('revision', views.nursing_revision, name='nursing_revision'),
    path('approved', views.nursing_approved, name='nursing_approved'),
    path('paid', views.nursing_paid, name='nursing_paid'),

    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('transactions', views.nursing_transactions, name='nursing_transactions'),
    
    
]