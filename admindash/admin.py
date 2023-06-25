from django.contrib import admin
from .models import Order, Writer, Editor, Client, Ordertracking, StatusLog, OrderFile, ChatMessage, Dashorderdetails, AdminOrderFile
# Register your models here.

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display=('id','orderNo', 'website', 'title',  'client', 'editor', 'writer', 'order_type',  'status', 'subject_area', 'academic_level','writer_level',
    'pages','sources', 'style', 'description','deadline', 'writer_time', 'price', 'writer_amount', 'editor_amount', 'net_amount',)
    list_display_links=('id',)
    search_fields=('title',)
    list_per_page=25

    search_fields = ("title__startswith", )
  
admin.site.register(Order, OrderAdmin)

class DashorderdetailsAdmin(admin.ModelAdmin):
    
    list_display=('id', 'order',  'status', 'client', 'writer', 'order_amount',
    'writer_amount','editor_amount','net_amount', 'date', )
    list_display_links=('id',)
    search_fields=('title',)
    list_per_page=25

    search_fields = ("title__startswith", )
  
admin.site.register(Dashorderdetails, DashorderdetailsAdmin)

class AdminOrderFileAdmin(admin.ModelAdmin):
    
    list_display=('id',  'order', 'file', 'editor', 'status', 'file_status', 'created_at', )
    list_display_links=('id',)
    search_fields=('order',)
    list_per_page=25

    search_fields = ("title__startswith", )
  
admin.site.register(AdminOrderFile, AdminOrderFileAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display=('id','client')
    list_display_links=('id', 'client')
    search_fields=('client',)
    list_per_page=25

    search_fields = ("client__startswith", )
  
admin.site.register(Client, ClientAdmin)

class EditorAdmin(admin.ModelAdmin):
    list_display=('id','editor')
    list_display_links=('id', 'editor')
    search_fields=('editor',)
    list_per_page=25

    search_fields = ("editor__startswith", )
  
admin.site.register(Editor, EditorAdmin)

class WriterAdmin(admin.ModelAdmin):
    list_display=('id', 'bio','writer','is_approved')
    list_display_links=('id',)
    search_fields=('writer',)
    list_per_page=25

    search_fields = ("writer__startswith", )
  
admin.site.register(Writer, WriterAdmin)

class OrdertrackingAdmin(admin.ModelAdmin):
    list_display=('id', 'order', 'status',  'remark', 'rating', 'UpdationDate','new_deadline', )
    list_display_links=('id',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("remark__startswith", )

admin.site.register(Ordertracking, OrdertrackingAdmin)

class StatusLogAdmin(admin.ModelAdmin):
    list_display=('id', 'order', 'old_status', 'new_status', 'date',)
    list_display_links=('id',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("order__startswith", )

admin.site.register(StatusLog, StatusLogAdmin)



class OrderFileAdmin(admin.ModelAdmin):
    list_display=('id', 'order', 'file', )
    list_display_links=('id',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("remark__startswith", )
  
admin.site.register(OrderFile, OrderFileAdmin)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display=('id', 'order',  'sender', 'sender_type', 'recipient_user', 'recipient_type', 'body', 'timestamp',)
    list_display_links=('id',   )
    search_fields=('order',)
    list_per_page=25

    search_fields = ("order__startswith", )
  
admin.site.register(ChatMessage, ChatMessageAdmin)