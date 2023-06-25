from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),

    path('nursinglogin',views.nursinglogin,name='nursinglogin'),
    path('nursinglogout',views.nursinglogout,name='nursinglogout'),
    path('nursingregister',views.nursingregister,name='nursingregister'),

    path('writerslogin',views.writerslogin,name='writerslogin'),
    path('writerslogout',views.writerslogout,name='writerslogout'),
    path('writersregister',views.writersregister,name='writersregister'),
   
   
]





