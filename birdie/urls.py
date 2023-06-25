from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orderform/', views.orderform, name='orderform'),
    path('order/<int:id>/', views.order, name='order'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('add_files/<int:id>/', views.add_files, name='add_files'),
    path('order/<int:order_id>/chat/', views.order_chat, name='order_chat'),
    path('order_messages/', views.order_messages, name='order_messages'),
    
]