from django.contrib import admin
from .models import BirdieOrder



class BirdieOrderAdmin(admin.ModelAdmin):
    list_display=('id', 'order', )
    list_display_links=('id', 'order',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("order__startswith", )
  
admin.site.register(BirdieOrder, BirdieOrderAdmin)