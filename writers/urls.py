from django.urls import path
from . import views



urlpatterns = [
    path('', views.writerdashboard, name='writerdashboard'),
    path('writerorder/<int:id>/', views.writerorder, name='writerorder'),
    path('upload_files/<int:id>/upload/', views.writer_upload_files, name='writer_upload_files'),
    path('bids/', views.bids, name='bids'),
    path('assigned_orders/', views.assigned_orders, name='assigned_orders'),
    path('editing_orders/', views.editing_orders, name='editing_orders'),
    path('completed_orders/', views.completed_orders, name='completed_orders'),
    path('revision_orders/', views.revision_orders, name='revision_orders'),
    path('approved_orders/', views.approved_orders, name='approved_orders'),
    path('clients_comments/', views.clients_comments, name='clients_comments'),
    
    
    path('order-filter/', views.order_filter, name='order_filter'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('orders/<int:id>/place_bid/', views.place_bid, name='place_bid'),
    path('orders/<str:level>/', views.filter_orders_by_level, name='filter_orders_by_level'),
]