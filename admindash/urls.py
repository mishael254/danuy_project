from django.urls import path

from . import views



urlpatterns = [

    path('', views.acade, name='acade'),
    path('admindashboard', views.admindashboard, name='admindashboard'),
    path('allorders', views.allorders, name='allorders'),
    path('adminorderdetails/<int:id>/', views.adminorderdetails, name='adminorderdetails'),
    path('adminpending', views.adminpending, name='adminpending'),
    path('adminavailable', views.adminavailable, name='adminavailable'),
    path('adminprogress', views.adminprogress, name='adminprogress'),
    path('admincompleted', views.admincompleted, name='admincompleted'),
    path('adminrevision', views.adminrevision, name='adminrevision'),
    path('admincancelled', views.admincancelled, name='admincancelled'),
    
    path('adminusers', views.adminusers, name='adminusers'),
    path('adminclients', views.adminclients, name='adminclients'),
    path('adminactivewriters', views.adminactivewriters, name='adminactivewriters'),
    path('adminapplicants', views.adminapplicants, name='adminapplicants'),
    path('admineditors', views.admineditors, name='admineditors'),
    
    path('adminedit_order/<int:id>/edit/', views.adminedit_order, name='adminedit_order'),
    path('admindelete_order/<int:id>/delete/', views.admindelete_order, name='admindelete_order'),
    path('adminbids', views.adminbids, name='adminbids'),
    path('adminorder_bids/<int:id>/bids/', views.adminorder_bids, name='adminorder_bids'),
    path('adminapproved', views.adminapproved, name='adminapproved'),
    path('order/<int:order_id>/assign-writer/<int:writer_id>/', views.assign_writer, name='assign_writer'),
    path('adminassigned', views.adminassigned, name='adminassigned'),
    path('adminediting', views.adminediting, name='adminediting'),
    path('upload_files/<int:id>/upload/', views.admin_upload_files, name='admin_upload_files'),
    
    
    path('download/<path:file_path>/', views.download_file, name='download_file'),


]