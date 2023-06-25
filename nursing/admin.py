from django.contrib import admin
from .models import NursingOrder, NursingContact, NursingSamples



class NursingOrderAdmin(admin.ModelAdmin):
    list_display=('id', 'order', )
    list_display_links=('id', 'order',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("order__startswith", )
  
admin.site.register(NursingOrder, NursingOrderAdmin)


class NursingContactAdmin(admin.ModelAdmin):
    list_display=('id', 'first_name','last_name', 'email', 'message', )
    list_display_links=('id', 'first_name',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("message__startswith", )
  
admin.site.register(NursingContact, NursingContactAdmin)

class NursingSamplesAdmin(admin.ModelAdmin):
    list_display=('id', 'sample_title','sample_file', 'sample_type', 'sample_subject_area', 'sample_academic_level', 'sample_pages','sample_sources', 'sample_style', 'sample_body','sample_price',)
    list_display_links=('id', 'sample_title',) 
    search_fields=('id',)
    list_per_page=25

    search_fields = ("sample_title", )
  
admin.site.register(NursingSamples, NursingSamplesAdmin)