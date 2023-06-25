from django.contrib import admin
from .models import WriterOrderFile, Bid, Writer


class WriterOrderFileAdmin(admin.ModelAdmin):
    list_display=('id', 'file','order','file_status','status',)
    list_display_links=('id',)
    search_fields=('order',)
    list_per_page=25

    search_fields = ("file__startswith", )
  
admin.site.register(WriterOrderFile, WriterOrderFileAdmin)




class BidAdmin(admin.ModelAdmin):
    list_display=('id', 'order','writer', 'amount', 'status','created_at',)
    list_display_links=('id', 'order','writer',)
    search_fields=('order',)
    list_per_page=25

    search_fields = ("order__startswith", )
  
admin.site.register(Bid, BidAdmin)